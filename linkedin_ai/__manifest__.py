{
    "name": "Create linkedin post with AI Chat GPT",
    "summary": """
        Create linkedin post with AI Chat GPT.""",
    "author": "Time to coode",
    "category": "base",
    "version": "17.0.0.1.1",
    "depends": ["web", "mail"],
    'external_dependencies':
        {
            'python': ['linkedin-api-client', 'openai'],
        },
    "data": [
        'data/ir_cron.xml',
        'views/res_company_view.xml',
        'views/linkedin_post.xml',
        'security/ir.model.access.csv',
    ],
}
