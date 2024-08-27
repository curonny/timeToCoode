from odoo import fields, models, api
import requests
from linkedin_api.clients.restli.client import RestliClient
import logging

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'
    _description = 'Description'

    linkedin_client_id = fields.Char('LinkedIn Client ID')
    linkedin_entity = fields.Char('LinkedIn Entity')
    linkedin_authorization_code = fields.Char('LinkedIn Authorization Code')
    linkedin_client_secret = fields.Char('LinkedIn Client Secret')
    gpt_api_key = fields.Char('Gpt Api Key')

    def linkedin_auth(self):
        try:
            restli_client = RestliClient()
            me = restli_client.get(
                resource_path="/me",
                access_token=self.linkedin_authorization_code
            )
            _logger.info(me.entity)
            self.update({'linkedin_entity': me.entity['id']})

        except Exception as e:
            print(e)

    def login_redirect_odoo(self):
        pass

    def get_linkedin_integration_data(self):
        return {
            'linkedin_client_id': self.linkedin_client_id,
            'linkedin_client_secret': self.linkedin_client_secret,
            'gpt_api_key': self.gpt_api_key
        }
