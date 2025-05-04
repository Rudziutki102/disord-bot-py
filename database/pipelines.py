report_pipeline = [
    {
        "$project": {
            "username": 1,
            "day": {
                "$dateToString": {
                    "format": "%Y-%m-%d",
                    "date": "$joined_at"
                }
            }
        }
    },
    {
        "$group": {
            "_id": "$username",
            "days": {"$addToSet": "$day"}
        }
    },
    {
        "$project": {
            "username": "$_id",
            "days": 1,
            "_id": 0
        }
    },
    {
        "$sort": {"username": 1}
    }
]
