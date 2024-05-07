### Profiles Collection Schema

```json
{
  "_id": "<MongoDB generated ObjectID>",
  "uuid": "7e86b06a-f896-4b4e-b7c4-7ab44fe42ab0",
  "name": "Rin",
  "role_uuid": "a24dff97-f8c7-49dd-9aa9-0ee93ad66891",
  "avatar": "haiku_female_15.png",
  "description": "Rin is a friendly but sometimes shy team lead.",
  "welcome_message": "Hey... I'm glad you're here.",
  "assistant_id": "<Unique identifier returned by OpenAI upon assistant creation>"
}
```

### Roles Collection Schema
```json
{
  "_id": "<MongoDB generated ObjectID>",
  "uuid": "a24dff97-f8c7-49dd-9aa9-0ee93ad66891",
  "name": "Default",
  "description": "General AI Agent",
  "model": "gpt-4-turbo",
  "instructions": "Specific behavior instructions.",
  "avatar": "bitbeard_profile.png",
  "tools": [
    "/core",
    "/agents",
    "/file_system",
    {
      "type": "file_search"
    }
  ]
}
```

### Teams Collection Schema
```json
{
  "_id": "<MongoDB generated ObjectID>",
  "uuid": "78cadd00-7b6b-426e-9c2e-7c17b95d77cf",
  "name": "Haiku DevOps",
  "description": "Team description.",
  "logo": "team-logo-1.png",
  "profile_uuids": [
    "7e86b06a-f896-4b4e-b7c4-7ab44fe42ab0",
    "b0a7b6df-50f8-4fbd-a365-53b480f24053",
    "f5c8e19d-a777-4d2b-b5ca-28bb9b7cf5f4"
  ]
}
```





