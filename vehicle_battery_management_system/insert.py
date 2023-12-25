# # main.py

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId
from typing import List
import json

app = FastAPI()

# MongoDB connection URL
MONGODB_URL = "mongodb+srv://<>:<>@cluster0.jwi0z9m.mongodb.net/?retryWrites=true&w=majority"

# MongoDB database name
DATABASE_NAME = "crud_example"

# MongoDB client
client = AsyncIOMotorClient(MONGODB_URL)

# MongoDB database
db = client[DATABASE_NAME]

# MongoDB collection
collection = db.get_collection("items")


class Item(BaseModel):
    name: str
    description: str


# Dependency to get the MongoDB client
async def get_database():
    return client


# Dependency to get the MongoDB collection
async def get_collection():
    return collection


# Create operation
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

@app.post("/items/", response_model=Item)
async def create_item(item: Item, db: AsyncIOMotorClient = Depends(get_database)):
    result = await db[DATABASE_NAME]["items"].insert_one(jsonable_encoder(item))
    created_item = await db[DATABASE_NAME]["items"].find_one({"_id": result.inserted_id})
    return JSONResponse(content=json.dumps(created_item, cls=CustomJSONEncoder))



# Read operation
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str, db: AsyncIOMotorClient = Depends(get_database)):
    item = await db[DATABASE_NAME]["items"].find_one({"_id": ObjectId(item_id)})
    if item:
        return item
    raise HTTPException(status_code=404, detail="Item not found")


# Read all operation
@app.get("/items/", response_model=List[Item])
async def read_items(db: AsyncIOMotorClient = Depends(get_database)):
    items = await db[DATABASE_NAME]["items"].find().to_list(1000)
    return JSONResponse(content=json.dumps(items, cls=CustomJSONEncoder))


# Update operation
@app.put("/items/{item_id}", response_model=Item)
async def update_item(
    item_id: str, item: Item, db: AsyncIOMotorClient = Depends(get_database)
):
    await db[DATABASE_NAME]["items"].update_one(
        {"_id": ObjectId(item_id)}, {"$set": jsonable_encoder(item)}
    )
    updated_item = await db[DATABASE_NAME]["items"].find_one(
        {"_id": ObjectId(item_id)}
    )
    if updated_item:
        return updated_item
    raise HTTPException(status_code=404, detail="Item not found")


# Delete operation
@app.delete("/items/{item_id}", response_model=Item)
async def delete_item(item_id: str, db: AsyncIOMotorClient = Depends(get_database)):
    deleted_item = await db[DATABASE_NAME]["items"].find_one_and_delete(
        {"_id": ObjectId(item_id)}
    )
    if deleted_item:
        return deleted_item
    raise HTTPException(status_code=404, detail="Item not found")


# # main.py

# from fastapi import FastAPI, Depends, HTTPException
# from fastapi.encoders import jsonable_encoder
# from motor.motor_asyncio import AsyncIOMotorClient
# from bson import ObjectId
# from pydantic import BaseModel
# from typing import List

# app = FastAPI()

# # Set arbitrary_types_allowed to True in the Config
# class Config:
#         arbitrary_types_allowed = True
#         json_encoders = {
#             ObjectId: lambda v: str(v)  # Convert ObjectId to string in Pydantic model
#         }
# newclass = Config()
# newclass.arbitrary_types_allowed = True

# # MongoDB connection URL
# MONGODB_URL = "mongodb://localhost:27017"

# # MongoDB database name
# DATABASE_NAME = "blog_db"

# # MongoDB client
# client = AsyncIOMotorClient(MONGODB_URL)

# # MongoDB database
# db = client[DATABASE_NAME]

# # Model for Comment with reference to Post
# class Comment(BaseModel):
#     user: str
#     text: str
#     post_id: ObjectId  # Reference to the corresponding post

# # Model for Post
# class Post(BaseModel):
#     title: str
#     content: str

# # Dependency to get the MongoDB client
# async def get_database():
#     return client

# # Dependency to get the MongoDB collection for posts
# async def get_posts_collection(db: AsyncIOMotorClient = Depends(get_database)):
#     return db[DATABASE_NAME]["posts"]

# # Dependency to get the MongoDB collection for comments
# async def get_comments_collection(db: AsyncIOMotorClient = Depends(get_database)):
#     return db[DATABASE_NAME]["comments"]

# # Create a new post
# @app.post("/posts/", response_model=Post)
# async def create_post(post: Post, posts_collection = Depends(get_posts_collection)):
#     post_dict = jsonable_encoder(post)
#     result = await posts_collection.insert_one(post_dict)
#     post_dict["_id"] = result.inserted_id
#     return post_dict

# # Create a new comment with reference to a post
# @app.post("/comments/", response_model=Comment)
# async def create_comment(comment: Comment, comments_collection = Depends(get_comments_collection)):
#     comment_dict = jsonable_encoder(comment)
#     result = await comments_collection.insert_one(comment_dict)
#     comment_dict["_id"] = result.inserted_id
#     return comment_dict

# # Retrieve a post with its comments
# @app.get("/posts/{post_id}", response_model=Post)
# async def read_post(post_id: ObjectId, posts_collection = Depends(get_posts_collection),
#                     comments_collection = Depends(get_comments_collection)):
#     post = await posts_collection.find_one({"_id": post_id})
#     if post:
#         comments = await comments_collection.find({"post_id": post_id}).to_list(1000)
#         post["comments"] = comments
#         return post
#     raise HTTPException(status_code=404, detail="Post not found")


# main.py

# from fastapi import FastAPI, Depends, HTTPException, Path
# from fastapi.encoders import jsonable_encoder
# from motor.motor_asyncio import AsyncIOMotorClient
# from bson import ObjectId
# from pydantic import BaseModel
# from typing import List

# from bson.objectid import ObjectId

# app = FastAPI()

# # MongoDB connection URL
# MONGODB_URL = "mongodb://localhost:27017"

# # MongoDB database name
# DATABASE_NAME = "blog_db"

# # MongoDB client
# client = AsyncIOMotorClient(MONGODB_URL)

# # MongoDB database
# db = client[DATABASE_NAME]

# # Model for Comment with reference to Post
# class Comment(BaseModel):
#     user: str
#     text: str
#     post_id: ObjectId  # Reference to the corresponding post

# # Model for Post
# class Post(BaseModel):
#     title: str
#     content: str

# # Dependency to get the MongoDB client
# async def get_database():
#     return client

# # Dependency to get the MongoDB collection for posts
# async def get_posts_collection(db: AsyncIOMotorClient = Depends(get_database)):
#     return db[DATABASE_NAME]["posts"]

# # Dependency to get the MongoDB collection for comments
# async def get_comments_collection(db: AsyncIOMotorClient = Depends(get_database)):
#     return db[DATABASE_NAME]["comments"]

# # Create a new post
# @app.post("/posts/", response_model=Post)
# async def create_post(post: Post, posts_collection = Depends(get_posts_collection)):
#     post_dict = jsonable_encoder(post)
#     result = await posts_collection.insert_one(post_dict)
#     post_dict["_id"] = result.inserted_id
#     return post_dict

# # Create a new comment with reference to a post
# @app.post("/comments/", response_model=Comment)
# async def create_comment(comment: Comment, comments_collection = Depends(get_comments_collection)):
#     comment_dict = jsonable_encoder(comment)
#     result = await comments_collection.insert_one(comment_dict)
#     comment_dict["_id"] = result.inserted_id
#     return comment_dict

# # Retrieve a post with its comments
# @app.get("/posts/{post_id}", response_model=Post)
# async def read_post(post_id: str = Path(..., title="The ID of the post"), posts_collection = Depends(get_posts_collection),
#                     comments_collection = Depends(get_comments_collection)):
#     post = await posts_collection.find_one({"_id": ObjectId(post_id)})
#     if post:
#         comments = await comments_collection.find({"post_id": ObjectId(post_id)}).to_list(1000)
#         post["comments"] = comments
#         return post
#     raise HTTPException(status_code=404, detail="Post not found")
