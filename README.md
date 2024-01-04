# calorie-counter
an LLM assisted calorie counter

# Work in progress
This is a work in progress. The goal is to start populating a food database using an LLM, and to let me track
my meals using a quick paragraph instead of obsessing over logging the exact portion size and type of food.
I accept that an LLM might halusinate and give me crazy data but I can fix it later if I care to. 

# Examples

## api request
```shell
curl http://127.0.0.1:5000/gpt \
  -d '{"message": "I had 3 olives in a teaspoon of super butter."}' \
  -H 'Content-Type: application/json; charset=utf-8' | \
jq '.choices[].message.content | fromjson'
```

## gpt request
```json
{
    "messages": [
        {
            "content": "\n        Create a json object with nutritional information about what is described to you. Sometimes\n        you will need to guess the nutritional information. For liquids prefer 100 grams. For example, \n        if a user wants to track a glass of milk, and there isn't the food item in the context. New \n        foods should also be updated when a new conversion is needed, but in that case you can skip\n        macros and calories if they are not changed. Example:\n        \n        \"A glass of milk and a cookie\"\n        \n        { \"new_foods\": [ {\n            \"name\": \"1% Milk\",\n            \"quantity\": 100,\n            \"quantity_units\": \"grams\",\n            \"calories\": 123.33333333333334,\n            \"conversions\": { \"cups\": 0.425 },\n            \"macros\": {\n                \"carbs\": 0.002,\n                \"fat\": 10.7,\n                \"protein\": 0.02\n            }, {\n            \"name\": \"Chocolate Chip Cookie\",\n            \"quantity\": 1,\n            \"quantity_units\": \"cookies\",\n            \"calories\": 4000,\n            \"conversions\": { \"grams\": 50 },\n            \"macros\": {\n                \"carbs\": 30,\n                \"fat\": 20,\n                \"protein\": 3\n            }\n        ], \"journal_entry\": [{\n                \"food\": \"milk\", \n                \"quantity\": 2,\n                \"quantity_units\": \"cups\",\n                \"comments\": [\"Assuming 1% milk\", \"Assuming a glass is 2 cups\"] \n            },\n            {\n                \"food\": \"cookie\", \n                \"quantity\": 1,\n                \"quantity_units\": \"cookies\",\n                \"comments\": [\"Assuming a 50g chocolate chip cookie\"] \n            }],\n          \"warnings\": []\n        }\n        \n        If all food that will be journaled is provided, just give an empty array of new foods. Warnings\n        can be given as an array of strings when there is a problem. Try to keep the response valid json.\n        ",
            "role": "system"
        },
        {
            "content": " Here are the foods I know of: \n[{'calories_per_gram': '44', 'food_id': 1624143566720362920, 'macros': {}, 'name': 'food', 'replacement_id': None}, {'calories_per_gram': '7.17', 'food_id': 1624143566720362921, 'macros': {'carbs': 0.001, 'fat': 0.822, 'protine': 0.009}, 'name': 'butter', 'replacement_id': None}, {'calories_per_gram': '123.33333333333334343434343434343434343434', 'food_id': 1624143566720362923, 'macros': {}, 'name': 'super-butter', 'replacement_id': None}, {'calories_per_gram': '123.33333333333334343434343434343434343434', 'food_id': 1624143566720362924, 'macros': [9.992992929929294], 'name': 'super-butter', 'replacement_id': None}]",
            "role": "user"
        },
        {
            "content": "Here is what I want to journal: \nI had 3 olives in a teaspoon of super butter.",
            "role": "user"
        }
    ],
    "model": "gpt-4"
}
```

## gpt response
```json
{
    "choices": [
        {
            "finish_reason": "stop",
            "index": 0,
            "logprobs": null,
            "message": {
                "content": "{\n    \"new_foods\": [\n        {\n            \"name\": \"Olives\",\n            \"quantity\": 1,\n            \"quantity_units\": \"olives\",\n            \"calories\": 25,\n            \"conversions\": { \"grams\": 4 },\n            \"macros\": {\n                \"carbs\": 0.03,\n                \"fat\": 2.3,\n                \"protein\": 0.11\n            }\n        }\n    ],\n    \"journal_entry\": [\n        {\n            \"food\": \"olives\",\n            \"quantity\": 3,\n            \"quantity_units\": \"olives\",\n            \"comments\": [\"Assuming each olive is approximately 4g\"]\n        },\n        {\n            \"food\": \"super-butter\",\n            \"quantity\": 1,\n            \"quantity_units\": \"teaspoon\",\n            \"comments\": [\"Assuming super-butter has similar nutritional values as normal butter\"]\n        }\n    ],\n    \"warnings\": []\n}",
                "role": "assistant"
            }
        }
    ],
    "created": 1704392137,
    "id": "chatcmpl-8dMXhwfDiCjoUYDG5oQ3xx9uMwedd",
    "model": "gpt-4-0613",
    "object": "chat.completion",
    "system_fingerprint": null,
    "usage": {
        "completion_tokens": 198,
        "prompt_tokens": 709,
        "total_tokens": 907
    }
}
```

## curl/jq response
```json
{
  "new_foods": [
    {
      "name": "Olives",
      "quantity": 1,
      "quantity_units": "olive",
      "calories": 8.2,
      "conversions": {
        "grams": 4.4
      },
      "macros": {
        "carbs": 0.49,
        "fat": 0.76,
        "protein": 0.08
      }
    },
    {
      "name": "Super Butter",
      "quantity": 100,
      "quantity_units": "grams",
      "calories": 123.33333333333334343434343434343434343434,
      "conversions": {
        "teaspoons": 14.3
      },
      "macros": {
        "carbs": 0.1,
        "fat": 99.3,
        "protein": 0.9
      }
    }
  ],
  "journal_entry": [
    {
      "food": "olives",
      "quantity": 3,
      "quantity_units": "olives",
      "comments": [
        "Assuming the olive is 2.2g and 8.2 calories per olive"
      ]
    },
    {
      "food": "super-butter",
      "quantity": 1,
      "quantity_units": "teaspoon",
      "comments": [
        "Assuming super butter has 124 calories per gram and a teaspoon weighs 14.3g"
      ]
    }
  ],
"warnings": [
    "The 'super-butter' in the database did not have 'macros' information"
  ]
}
```
