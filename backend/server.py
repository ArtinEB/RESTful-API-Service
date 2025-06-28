import os
import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pymongo import MongoClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="E-commerce API",
    description="A comprehensive RESTful API for e-commerce product management",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'ecommerce_db')

try:
    client = MongoClient(MONGO_URL)
    db = client[DB_NAME]
    products_collection = db.products
    logger.info(f"Connected to MongoDB at {MONGO_URL}")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    raise

# Pydantic models
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Product name")
    description: str = Field(..., min_length=1, max_length=1000, description="Product description")
    price: float = Field(..., gt=0, description="Product price (must be positive)")
    category: str = Field(..., min_length=1, max_length=100, description="Product category")
    stock_quantity: int = Field(..., ge=0, description="Stock quantity (non-negative)")
    image_url: Optional[str] = Field(None, description="Product image URL")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    stock_quantity: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = None

class Product(ProductBase):
    id: str = Field(..., description="Unique product identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

# Helper functions
def product_helper(product) -> dict:
    """Convert MongoDB document to Product dict"""
    return {
        "id": product["id"],
        "name": product["name"],
        "description": product["description"],
        "price": product["price"],
        "category": product["category"],
        "stock_quantity": product["stock_quantity"],
        "image_url": product.get("image_url"),
        "created_at": product["created_at"],
        "updated_at": product["updated_at"]
    }

# API Endpoints

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "E-commerce API",
        "version": "1.0.0",
        "documentation": "Access Swagger docs at: /docs or see OpenAPI spec at /openapi.json",
        "endpoints": {
            "products": "/api/products",
            "health": "/api/health"
        }
    }

@app.get("/api/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        db.command('ping')
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}"
        )

@app.post("/api/products", response_model=Product, status_code=status.HTTP_201_CREATED, tags=["Products"])
async def create_product(product: ProductCreate):
    """Create a new product"""
    try:
        product_id = str(uuid.uuid4())
        current_time = datetime.utcnow()
        
        product_dict = product.dict()
        product_dict.update({
            "id": product_id,
            "created_at": current_time,
            "updated_at": current_time
        })
        
        result = products_collection.insert_one(product_dict)
        
        if result.inserted_id:
            created_product = products_collection.find_one({"id": product_id})
            return product_helper(created_product)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create product"
            )
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create product: {str(e)}"
        )

@app.get("/api/products", response_model=List[Product], tags=["Products"])
async def get_products(skip: int = 0, limit: int = 50, category: Optional[str] = None):
    """Get all products with optional filtering and pagination"""
    try:
        query = {}
        if category:
            query["category"] = {"$regex": category, "$options": "i"}
        
        products = list(
            products_collection.find(query)
            .skip(skip)
            .limit(limit)
            .sort("created_at", -1)
        )
        
        return [product_helper(product) for product in products]
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch products: {str(e)}"
        )

@app.get("/api/products/{product_id}", response_model=Product, tags=["Products"])
async def get_product(product_id: str):
    """Get a specific product by ID"""
    try:
        product = products_collection.find_one({"id": product_id})
        
        if product:
            return product_helper(product)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching product {product_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch product: {str(e)}"
        )

@app.put("/api/products/{product_id}", response_model=Product, tags=["Products"])
async def update_product(product_id: str, product_update: ProductUpdate):
    """Update a specific product"""
    try:
        existing_product = products_collection.find_one({"id": product_id})
        
        if not existing_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found"
            )
        
        # Only update fields that are provided
        update_data = {}
        for field, value in product_update.dict(exclude_unset=True).items():
            if value is not None:
                update_data[field] = value
        
        if update_data:
            update_data["updated_at"] = datetime.utcnow()
            
            result = products_collection.update_one(
                {"id": product_id},
                {"$set": update_data}
            )
            
            if result.modified_count == 1:
                updated_product = products_collection.find_one({"id": product_id})
                return product_helper(updated_product)
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update product"
                )
        else:
            # No updates provided, return existing product
            return product_helper(existing_product)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating product {product_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update product: {str(e)}"
        )

@app.delete("/api/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Products"])
async def delete_product(product_id: str):
    """Delete a specific product"""
    try:
        result = products_collection.delete_one({"id": product_id})
        
        if result.deleted_count == 1:
            return None
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting product {product_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete product: {str(e)}"
        )

@app.get("/api/products/category/{category}", response_model=List[Product], tags=["Products"])
async def get_products_by_category(category: str, skip: int = 0, limit: int = 50):
    """Get products filtered by category"""
    try:
        products = list(
            products_collection.find({"category": {"$regex": category, "$options": "i"}})
            .skip(skip)
            .limit(limit)
            .sort("created_at", -1)
        )
        
        return [product_helper(product) for product in products]
    except Exception as e:
        logger.error(f"Error fetching products by category {category}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch products by category: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)