from odoo import fields, models, api
from linkedin_api.clients.restli.client import RestliClient
import logging
from datetime import datetime, timedelta
from openai import OpenAI
import os

_logger = logging.getLogger(__name__)


class LinkedinPost(models.Model):
    _name = 'linkedin.post'
    _inherit = ['mail.thread']
    _description = 'Description'

    name = fields.Char(tracking=True)
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    description = fields.Text(tracking=True)
    body = fields.Html()
    frequency = fields.Selection([('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], default='weekly',
                                 tracking=True)
    date_post = fields.Date(tracking=True, required=True, default=datetime.now())
    next_date = fields.Date(tracking=True)

    def apply_frequency(self):
        self.update({'date_post': datetime.utcnow()})
        if self.frequency == 'daily':
            self.update({'next_date': self.date_post + timedelta(days=1)})
        elif self.frequency == 'weekly':
            self.update({'next_date': self.date_post + timedelta(weeks=1)})
        elif self.frequency == 'monthly':
            self.update({'next_date': self.date_post + timedelta(days=30)})

    def check_linkedin_post(self):
        posts = self.env['linkedin.post'].search([('next_date', '==', datetime.utcnow().date())])
        for post in posts:
            post.do_linkedin_post()

    def get_post_body(self):
        client = OpenAI(
            api_key=self.company_id.gpt_api_key
        )
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Escribe un resumen corto para linkedin sobre {self.description}",
                }
            ],
            model="gpt-3.5-turbo",
        )

        return chat_completion.choices[0].message.content

    def publish_linkedin_post(self):
        try:
            restli_client = RestliClient()
            _logger.info(len(self.body))
            response = restli_client.create(
                resource_path="/posts",
                entity={
                    "author": f"urn:li:person:{self.company_id.linkedin_entity}",
                    "lifecycleState": "PUBLISHED",
                    "visibility": "PUBLIC",
                    "commentary": self.body.replace('<p>', '').replace('</p>', ''),
                    "distribution": {
                        "feedDistribution": "MAIN_FEED",
                        "targetEntities": [],
                        "thirdPartyDistributionChannels": [],
                    },

                },
                access_token=self.company_id.linkedin_authorization_code,
            )
            if response.status_code == 201:
                _logger.info(response)
                self.apply_frequency()
            else:
                _logger.info(response.entity)
                self.message_post(body=response.entity)
        except Exception as e:
            print(e)

    def do_linkedin_post(self):
        self.ensure_one()
        self.update({'body': self.get_post_body()})
        self.publish_linkedin_post()
