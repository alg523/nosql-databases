from pymongo import MongoClient
import pprint

client = MongoClient()
db = client.movies
collection = db.movies
collection_2 = db.ticketSales
collection_3 = db.ticketPrices



#Part A
collection.update_many({"rated":"NOT RATED"}, {"$set":{"rated":"Pending rating"}})


#Part B
collection.insert_one(
     {"title": "A Quiet Place",
      "year": 2018,
      "countries": ["USA"],
      "genres": ["Drama", "Horror", "Sci-Fi"],
      "directors": ["John Krasinski"],
      "imdb": {"id": 500,
               "rating": 8.1,
               "votes": 55588}
     }
)


#Part C
drama_total = collection.aggregate( [
                        { "$unwind": "$genres"},
                        { "$match": {"genres": "Drama" } },
                        { "$group": { "_id": "$genres", "count": { "$sum": 1}}}
                      ]
                    ) 
print(list(drama_total))


#Part D
usa_total = collection.aggregate( [
                                    { "$unwind": "$countries"},
                                    { "$match": { "countries": "USA", "rated": "Pending rating" } },
                                    { "$group": { "_id": { "country" : "$countries", "rated": "$rated"}, "count": {"$sum": 1}}}
                                  ]
                                )
print(list(usa_total))


#Part E
collection_2.insert_many( [
                           {"transaction_id": 1, "day_total": 50000, "hour_sales": 2000},
                           {"transaction_id": 2, "day_total": 70000, "hour_sales": 3000},
                           {"transaction_id": 3, "day_total": 40000, "hour_sales": 1000}
                          ]
                        )

collection_3.insert_many( [
                           {"price_id": 3, "normal_prices": 14, "imax_prices": 20},
                           {"price_id": 2, "normal_prices": 11, "imax_prices": 17},
                           {"price_id": 1, "normal_prices": 12, "imax_prices": 18}
                          ]
                        )

lookup_example = collection_2.aggregate( [
                                          { "$lookup": { "from": "ticketPrices", "localField": "transaction_id", "foreignField": "price_id", "as": "prices" } }
                                         ]
                                       )
#I used the pprint package here to make the output a bit more readable 
pprint.pprint(list(lookup_example))
