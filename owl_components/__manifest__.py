{
    "name": "OWL Components",
    "summary": """
        Add item to favorite and recent list.""",
    "author": "Time to coode",
    "category": "POS",
    "version": "17.0.0.1.0",
    "depends": ["web"],
    "data": [
        "views/ir_actions_client.xml",
    ],
    "assets": {
        "web.assets_backend": ["owl_components/static/src/**/*"],
    },
}
