# E-commerce API Project

A comprehensive RESTful API for e-commerce product management built with FastAPI, React, and MongoDB.

## 🚀 Overview

This project demonstrates a complete e-commerce API with full CRUD operations for product management. It includes both a robust backend API and a beautiful frontend interface for managing products.

### Key Features

- ✅ **Complete CRUD Operations** for products
- ✅ **RESTful API Design** with proper HTTP methods and status codes
- ✅ **Input Validation** with comprehensive error handling
- ✅ **Interactive Documentation** with Swagger/OpenAPI
- ✅ **Modern Frontend Interface** with React and Tailwind CSS
- ✅ **Real-time Updates** and responsive design
- ✅ **Production-ready** with proper logging and monitoring

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **MongoDB** - NoSQL database for flexible data storage
- **Pydantic** - Data validation and settings management
- **Python 3.9+** - Programming language

### Frontend
- **React** - JavaScript library for building user interfaces
- **Tailwind CSS** - Utility-first CSS framework
- **JavaScript ES6+** - Modern JavaScript features

### Infrastructure
- **Docker** - Containerization
- **Supervisor** - Process management
- **Kubernetes** - Container orchestration (production)

## 📚 API Documentation

### Base URL
```
https://api.example.com/api
```

### Core Endpoints

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|-------------|
| `GET` | `/api/health` | Health check | 200 |
| `POST` | `/api/products` | Create product | 201 |
| `GET` | `/api/products` | List all products | 200 |
| `GET` | `/api/products/{id}` | Get specific product | 200 |
| `PUT` | `/api/products/{id}` | Update product | 200 |
| `DELETE` | `/api/products/{id}` | Delete product | 204 |
| `GET` | `/api/products/category/{category}` | Get products by category | 200 |

### Product Model

```json
{
  "id": "uuid-string",
  "name": "string (required, 1-200 chars)",
  "description": "string (required, 1-1000 chars)",
  "price": "float (required, > 0)",
  "category": "string (required, 1-100 chars)",
  "stock_quantity": "integer (required, >= 0)",
  "image_url": "string (optional)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## 🔧 API Usage Examples

### Create a Product
```bash
curl -X POST "https://api.example.com/api/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Bluetooth Headphones",
    "description": "Premium quality wireless headphones with noise cancellation",
    "price": 129.99,
    "category": "Electronics",
    "stock_quantity": 50,
    "image_url": "https://example.com/headphones.jpg"
  }'
```

### Get All Products
```bash
curl -X GET "https://api.example.com/api/products"
```

### Get Products with Pagination
```bash
curl -X GET "https://api.example.com/api/products?skip=0&limit=10"
```

### Get Product by ID
```bash
curl -X GET "https://api.example.com/api/products/{product-id}"
```

### Update a Product
```bash
curl -X PUT "https://api.example.com/api/products/{product-id}" \
  -H "Content-Type: application/json" \
  -d '{
    "price": 119.99,
    "stock_quantity": 45
  }'
```

### Delete a Product
```bash
curl -X DELETE "https://api.example.com/api/products/{product-id}"
```

### Filter by Category
```bash
curl -X GET "https://api.example.com/api/products/category/Electronics"
```

## 🖥️ Frontend Interface

Access the product management interface at:
```
https://yourapp.example.com
```

### Features
- **Product Listing** - View all products with images, prices, and stock status
- **Create Products** - Add new products with full form validation
- **Edit Products** - Update existing product information
- **Delete Products** - Remove products with confirmation dialogs
- **Responsive Design** - Works on desktop, tablet, and mobile devices
- **Real-time Updates** - UI updates immediately after operations

## 🏗️ Project Structure

```
/app/
├── backend/                    # FastAPI backend
│   ├── server.py              # Main FastAPI application
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   ├── App.css           # Component styles
│   │   ├── index.js          # Entry point
│   │   └── index.css         # Global styles
│   ├── public/               # Static assets
│   ├── package.json          # Node.js dependencies
│   ├── tailwind.config.js    # Tailwind CSS configuration
│   └── .env                  # Environment variables
├── tests/                    # Test files
├── scripts/                  # Utility scripts
└── README.md                # This file
```

## 🔍 Interactive Documentation

### Swagger UI
Access the interactive API documentation at:
```
https://yourapp.example.com/docs
```

### OpenAPI Schema
Get the OpenAPI JSON schema at:
```
https://yourapp.example.com/openapi.json
```

## 🧪 Testing

The project includes comprehensive test coverage:

### Backend API Tests
- ✅ All CRUD operations
- ✅ Input validation and error handling
- ✅ Edge cases and concurrent operations
- ✅ Database integration
- ✅ Health checks

### Frontend Tests
- ✅ Component rendering
- ✅ Form interactions
- ✅ API integration
- ✅ Error handling
- ✅ Responsive design

### Test Results
All tests pass successfully, confirming:
- API endpoints work correctly
- Frontend integrates seamlessly with backend
- Data persistence across operations
- Proper error handling and validation

## 🚦 Status Codes

| Code | Description |
|------|-------------|
| `200` | Success (GET, PUT) |
| `201` | Created (POST) |
| `204` | No Content (DELETE) |
| `400` | Bad Request (validation errors) |
| `404` | Not Found (invalid ID) |
| `422` | Unprocessable Entity (validation errors) |
| `500` | Internal Server Error |

## 🔧 Development Setup

### Prerequisites
- Python 3.9+
- Node.js 16+
- MongoDB
- Docker (optional)

### Local Development

1. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   python server.py
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   yarn install
   yarn start
   ```

3. **Database Setup**
   - MongoDB running on `mongodb://localhost:27017`
   - Database name: `ecommerce_db`

### Environment Variables

**Backend (.env)**
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=ecommerce_db
```

**Frontend (.env)**
```
REACT_APP_BACKEND_URL=https://yourapi.example.com
```

## 🛡️ Security Features

- Input validation with Pydantic models
- SQL injection prevention (NoSQL MongoDB)
- CORS configuration for cross-origin requests
- Proper error handling without sensitive data exposure
- UUID-based IDs (non-sequential, secure)

## 📈 Performance Features

- Efficient MongoDB queries with indexing
- Pagination for large datasets
- Async/await for non-blocking operations
- Optimized frontend rendering with React
- CDN-ready static assets

## 🚀 Production Deployment

The application is containerized and ready for production deployment:

- **Docker containers** for both frontend and backend
- **Kubernetes configuration** for scalability
- **Supervisor process management** for reliability
- **Load balancer ready** with proper health checks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

For support and questions:
- Check the interactive API documentation at `/docs`
- Review the test cases for usage examples
- Examine the frontend implementation for integration patterns

## 🎯 Next Steps

Potential enhancements for this API:
- **Authentication & Authorization** (JWT tokens, user roles)
- **Order Management** (shopping cart, checkout process)
- **Payment Integration** (Stripe, PayPal)
- **Inventory Management** (low stock alerts, batch updates)
- **Search & Filtering** (full-text search, advanced filters)
- **Image Upload** (file handling, image optimization)
- **Caching** (Redis for improved performance)
- **Rate Limiting** (API usage controls)
- **Monitoring** (logging, metrics, alerting)

---

**Built with ❤️ using FastAPI, React, and MongoDB**