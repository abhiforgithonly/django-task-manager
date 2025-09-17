# 🚀 Django Task Manager with Third-Party API Integration

A comprehensive Django web application demonstrating CRUD operations, third-party API integration, and data visualization using PostgreSQL (Supabase) as the database backend.

## 📋 Project Overview

This application fulfills the following requirements:
- ✅ **CRUD Operations**: Complete Create, Read, Update, Delete functionality via REST APIs
- ✅ **Third-Party API Integration**: Real-time weather data from OpenWeatherMap API
- ✅ **Data Visualization**: Interactive charts and analytics dashboard with task statistics
- ✅ **PostgreSQL Integration**: Uses Supabase (PostgreSQL) for robust data storage
- ✅ **Modern UI**: Responsive web interface with real-time updates

## ✨ Core Features

### 📝 CRUD Operations (REST API)
- **Create Tasks**: POST `/api/tasks/` - Add new tasks with title, description, priority, status
- **Read Tasks**: GET `/api/tasks/` - Retrieve all tasks with filtering options
- **Update Tasks**: PUT `/api/tasks/{id}/` - Modify existing tasks
- **Delete Tasks**: DELETE `/api/tasks/{id}/` - Remove tasks from database

### 🌐 Third-Party API Integration
- **OpenWeatherMap API**: Real-time weather data retrieval
- **Weather Logging**: Automatic storage of weather queries in database
- **City-based Weather**: Support for global city weather lookup
- **Error Handling**: Robust error handling for API failures

### 📊 Data Visualization & Reporting
- **Task Analytics**: Visual charts showing task completion rates
- **Priority Distribution**: Bar charts displaying task priority breakdown
- **Status Tracking**: Pie charts for task status distribution
- **Real-time Statistics**: Dynamic calculation of completion rates and metrics
- **Chart Generation**: Server-side chart creation using Matplotlib

## 🛠️ Technology Stack

- **Backend**: Django 5.1, Django REST Framework
- **Database**: Supabase (PostgreSQL)
- **Third-Party API**: OpenWeatherMap API
- **Visualization**: Matplotlib (server-side), JavaScript (client-side)
- **Frontend**: HTML5, CSS3, JavaScript (ES6), Axios
- **Styling**: Custom CSS with modern design principles

## 🏗️ API Architecture

### REST API Endpoints

| Method | Endpoint | Description | CRUD Operation |
|--------|----------|-------------|----------------|
| `GET` | `/api/tasks/` | List all tasks | **Read** |
| `POST` | `/api/tasks/` | Create new task | **Create** |
| `GET` | `/api/tasks/{id}/` | Get specific task | **Read** |
| `PUT` | `/api/tasks/{id}/` | Update task | **Update** |
| `DELETE` | `/api/tasks/{id}/` | Delete task | **Delete** |
| `GET` | `/api/weather/{city}/` | Get weather data | **Third-Party API** |
| `GET` | `/api/analytics/` | Get data visualization | **Reporting** |

### API Request/Response Examples

**Create Task (POST /api/tasks/)**
```json
{
  "title": "Complete project documentation",
  "description": "Write comprehensive README and API docs",
  "priority": "high",
  "status": "pending",
  "user": 1
}
```

**Weather API (GET /api/weather/Mumbai/)**
```json
{
  "city": "Mumbai",
  "temperature": 28.5,
  "description": "clear sky",
  "humidity": 65,
  "logged_at": "2024-09-17T10:30:00Z",
  "feels_like": 31.2
}
```

## 📁 Project Structure

```
taskmanager/
├── taskmanager/
│   ├── settings.py          # Django configuration
│   ├── urls.py              # Main URL routing
│   └── wsgi.py              # WSGI configuration
├── tasks/
│   ├── models.py            # Database models (Task, WeatherLog)
│   ├── views.py             # API views and business logic
│   ├── serializers.py       # DRF serializers for API
│   ├── app_urls.py          # Application URL patterns
│   └── admin.py             # Django admin interface
├── templates/
│   └── dashboard.html       # Frontend dashboard
├── requirements.txt         # Python dependencies
├── .env                     # Environment configuration
└── README.md                # Project documentation
```

## 🗄️ Database Schema

### Task Model
```python
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(choices=['low', 'medium', 'high'])
    status = models.CharField(choices=['pending', 'in_progress', 'completed'])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
```

### WeatherLog Model
```python
class WeatherLog(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    description = models.CharField(max_length=200)
    humidity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ installed on your system
- pip package manager
- Supabase account and database (free at [supabase.com](https://supabase.com))
- OpenWeatherMap API key (free at [openweathermap.org](https://openweathermap.org/api))

### Installation

1. **Clone or download the project**
   ```bash
   cd "Django task App"
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django djangorestframework python-decouple requests matplotlib dj-database-url django-cors-headers psycopg2-binary
   ```

4. **Set up Supabase database**
   
   - Go to [supabase.com](https://supabase.com) and create a free account
   - Create a new project
   - Go to Settings → Database
   - Copy your database URL (it looks like: `postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres`)

5. **Create environment file**
   
   Create a `.env` file in the project root with:
   ```env
   SECRET_KEY=your-super-secret-key-here
   DEBUG=True
   DATABASE_URL=postgresql://postgres:[YOUR_PASSWORD]@[YOUR_HOST]:5432/postgres
   WEATHER_API_KEY=your-openweathermap-api-key-here
   ```

   **Generate a Django Secret Key:**
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   Copy the output and replace `your-super-secret-key-here` with it.

   **Get your Database URL from Supabase:**
   - Go to your Supabase project dashboard
   - Navigate to Settings → Database
   - Copy the connection string under "Connection string" → "URI"
   - Replace `[YOUR_PASSWORD]` with your database password
   - Replace `[YOUR_HOST]` with your database host

   **Get your Weather API Key:**
   - Visit [OpenWeatherMap](https://openweathermap.org/api)
   - Sign up for a free account
   - Generate an API key
   - Replace `your-openweathermap-api-key-here` with your actual key

6. **Set up the database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
   
   *Note: Your tables will be created in your Supabase database. You can view them in the Supabase dashboard under "Table Editor".*

7. **Create a superuser** (optional)
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Open your browser**
   
   Navigate to: `http://localhost:8000`

## 🧪 Testing the Application

### CRUD Operations Testing

1. **Create (POST)**
   ```bash
   curl -X POST http://localhost:8000/api/tasks/ \
   -H "Content-Type: application/json" \
   -d '{
     "title": "Test Task",
     "description": "Testing CRUD operations",
     "priority": "medium",
     "status": "pending",
     "user": 1
   }'
   ```

2. **Read (GET)**
   ```bash
   # Get all tasks
   curl http://localhost:8000/api/tasks/
   
   # Get specific task
   curl http://localhost:8000/api/tasks/1/
   
   # Filter tasks by status
   curl http://localhost:8000/api/tasks/?status=pending
   ```

3. **Update (PUT)**
   ```bash
   curl -X PUT http://localhost:8000/api/tasks/1/ \
   -H "Content-Type: application/json" \
   -d '{
     "title": "Updated Task",
     "description": "Updated description",
     "priority": "high",
     "status": "completed",
     "user": 1
   }'
   ```

4. **Delete (DELETE)**
   ```bash
   curl -X DELETE http://localhost:8000/api/tasks/1/
   ```

### Third-Party API Integration Testing

```bash
# Test weather API integration
curl http://localhost:8000/api/weather/Mumbai/
curl http://localhost:8000/api/weather/London/
curl http://localhost:8000/api/weather/Tokyo/
```

### Data Visualization Testing

```bash
# Test analytics and reporting
curl http://localhost:8000/api/analytics/
```

## 📊 Data Visualization Features

### Analytics Dashboard
- **Task Completion Rate**: Percentage of completed vs total tasks
- **Priority Distribution**: Bar chart showing task priorities
- **Status Breakdown**: Pie chart of task statuses
- **Recent Activity**: List of recently created/updated tasks
- **Weather Integration History**: Log of weather API calls

### Chart Types
- **Pie Charts**: Task status distribution
- **Bar Charts**: Priority levels and completion trends
- **Statistics Cards**: Key metrics and KPIs
- **Base64 Images**: Server-generated charts for immediate display

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Django secret key (generate with command above) | Yes | `django-insecure-abc123...` |
| `DEBUG` | Debug mode | No | `True` (dev), `False` (prod) |
| `DATABASE_URL` | Supabase connection string | Yes | `postgresql://postgres:password@host:5432/postgres` |
| `WEATHER_API_KEY` | OpenWeatherMap API key | Yes | `abcd1234567890abcd...` |

### Database Configuration

**Supabase:**
```env
DATABASE_URL=postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres
```

### Supabase Setup Details

1. **Create Supabase Project:**
   - Visit [supabase.com](https://supabase.com)
   - Click "New Project"
   - Choose your organization and project name
   - Select a region close to your users
   - Set a strong database password

2. **Get Connection Details:**
   - Go to Settings → Database
   - Find "Connection string" section
   - Copy the URI format connection string
   - Replace `[YOUR-PASSWORD]` with your actual password

3. **View Your Data:**
   - Use the Table Editor in Supabase dashboard
   - View your `tasks_task` and `tasks_weatherlog` tables
   - Monitor real-time data changes

## 🚨 Troubleshooting

### Common Issues

1. **Database connection issues**
   - Verify your Supabase DATABASE_URL in `.env`
   - Check if your Supabase project is active
   - Ensure your IP is allowed (Supabase → Settings → Database → Network Restrictions)
   - Test connection: `curl http://localhost:8000/api/debug-config/`

2. **Weather API not working**
   - Check your `WEATHER_API_KEY` in `.env`
   - Verify the API key is valid at OpenWeatherMap
   - Test with: `curl http://localhost:8000/api/debug-config/`

3. **Tasks not saving**
   - Check Supabase database connection
   - Verify migrations were applied: `python manage.py migrate`
   - Check Supabase dashboard → Table Editor for `tasks_task` table
   - Look for errors in browser developer tools

4. **Charts not displaying**
   - Ensure matplotlib is installed: `pip install matplotlib`
   - Check if tasks exist in database
   - Verify analytics endpoint: `curl http://localhost:8000/api/analytics/`

5. **Server not starting**
   - Check if port 8000 is available
   - Verify all dependencies are installed: `pip list`
   - Check `.env` file format and Supabase connection
   - Ensure `psycopg2-binary` is installed for PostgreSQL

### Debug Commands

```bash
# Check system configuration
curl http://localhost:8000/api/debug-config/

# Run Django checks
python manage.py check

# View Django logs
python manage.py runserver --verbosity=2

# Test database connection with Supabase
python manage.py shell
>>> from tasks.models import Task
>>> Task.objects.count()  # Should return number without errors

# Check Supabase connection specifically
python manage.py dbshell  # Should connect to your Supabase database
```

## 📱 Browser Compatibility

- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 🔒 Security Notes

- Never commit your `.env` file to version control
- Generate a unique `SECRET_KEY` using the command provided above
- Use strong, unique `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Configure proper CORS settings for production
- Keep your Supabase database password secure
- Use Supabase Row Level Security (RLS) for production apps

## 💾 Database Management

### Viewing Your Data
- **Supabase Dashboard**: Go to Table Editor to view/edit data
- **Django Admin**: Access at `http://localhost:8000/admin/` (after creating superuser)
- **API Endpoints**: Use the REST API to manage data programmatically

### Backup & Migration
- **Supabase**: Automatic backups available in dashboard
- **Local Backup**: Use `python manage.py dumpdata` for Django fixtures
- **Migration**: Standard Django migrations work with Supabase

## 🎯 Project Requirements Fulfilled

### ✅ CRUD Operations via REST APIs
- Complete Create, Read, Update, Delete functionality
- RESTful API design with proper HTTP methods
- JSON request/response format
- Error handling and validation
- Filtering and querying capabilities

### ✅ Third-Party API Integration
- OpenWeatherMap API integration for real-time weather data
- Automatic data logging to database
- Error handling for API failures
- Multiple city support with global coverage

### ✅ Data Visualization & Reporting
- Interactive charts and graphs
- Task completion analytics
- Priority distribution visualization
- Real-time statistics calculation
- Server-side chart generation with Matplotlib

### ✅ PostgreSQL Integration
- Supabase (PostgreSQL) database backend
- Proper database modeling and relationships
- Migration system for schema management
- Connection pooling and optimization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Verify your `.env` configuration
3. Test API endpoints individually
4. Check browser console for JavaScript errors

---

**Happy Development! 🎉**

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ installed on your system
- pip package manager
- Supabase account and database (free at [supabase.com](https://supabase.com))
- OpenWeatherMap API key (free at [openweathermap.org](https://openweathermap.org/api))

### Installation

1. **Clone or download the project**
   ```bash
   cd "Django task App"
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django djangorestframework python-decouple requests matplotlib dj-database-url django-cors-headers psycopg2-binary
   ```

4. **Set up Supabase database**
   
   - Go to [supabase.com](https://supabase.com) and create a free account
   - Create a new project
   - Go to Settings → Database
   - Copy your database URL (it looks like: `postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres`)

5. **Create environment file**
   
   Create a `.env` file in the project root with:
   ```env
   SECRET_KEY=your-super-secret-key-here
   DEBUG=True
   DATABASE_URL=postgresql://postgres:[YOUR_PASSWORD]@[YOUR_HOST]:5432/postgres
   WEATHER_API_KEY=your-openweathermap-api-key-here
   ```

   **Generate a Django Secret Key:**
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   Copy the output and replace `your-super-secret-key-here` with it.

   **Get your Database URL from Supabase:**
   - Go to your Supabase project dashboard
   - Navigate to Settings → Database
   - Copy the connection string under "Connection string" → "URI"
   - Replace `[YOUR_PASSWORD]` with your database password
   - Replace `[YOUR_HOST]` with your database host

   **Get your Weather API Key:**
   - Visit [OpenWeatherMap](https://openweathermap.org/api)
   - Sign up for a free account
   - Generate an API key
   - Replace `your-openweathermap-api-key-here` with your actual key

6. **Set up the database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
   
   *Note: Your tables will be created in your Supabase database. You can view them in the Supabase dashboard under "Table Editor".*

7. **Create a superuser** (optional)
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Open your browser**
   
   Navigate to: `http://localhost:8000`

## 🧪 Testing the Application

### Manual Testing

1. **Dashboard Access**
   - Visit `http://localhost:8000`
   - You should see the beautiful task manager dashboard

2. **Task Management**
   - Create a new task using the form
   - View tasks in the tasks list
   - Filter tasks by status
   - Delete tasks using the delete button

3. **Weather Feature**
   - Enter a city name (e.g., "Mumbai", "New York", "London")
   - Click "Get Weather" to fetch real-time data
   - Weather data should display with temperature, humidity, etc.

4. **Analytics**
   - Click "Load Analytics" to generate charts
   - View task statistics and visual charts
   - Check completion rates and priority distribution

### API Testing

Test the REST API endpoints using curl or a tool like Postman:

```bash
# Test tasks endpoint
curl http://localhost:8000/api/tasks/

# Test weather endpoint
curl http://localhost:8000/api/weather/Mumbai/

# Test analytics endpoint
curl http://localhost:8000/api/analytics/

# Test configuration
curl http://localhost:8000/api/debug-config/
```

### Available API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/tasks/` | GET, POST | List/Create tasks |
| `/api/tasks/{id}/` | GET, PUT, DELETE | Retrieve/Update/Delete task |
| `/api/weather/{city}/` | GET | Get weather for city |
| `/api/analytics/` | GET | Get task analytics and charts |
| `/api/test/` | GET | Test endpoint connectivity |
| `/api/debug-config/` | GET | Debug configuration status |

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Django secret key (generate with command above) | Yes | `django-insecure-abc123...` |
| `DEBUG` | Debug mode | No | `True` (dev), `False` (prod) |
| `DATABASE_URL` | Supabase connection string | Yes | `postgresql://postgres:password@host:5432/postgres` |
| `WEATHER_API_KEY` | OpenWeatherMap API key | Yes | `abcd1234567890abcd...` |

### Database Configuration

**Supabase:**
```env
DATABASE_URL=postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres
```

### Supabase Setup Details

1. **Create Supabase Project:**
   - Visit [supabase.com](https://supabase.com)
   - Click "New Project"
   - Choose your organization and project name
   - Select a region close to your users
   - Set a strong database password

2. **Get Connection Details:**
   - Go to Settings → Database
   - Find "Connection string" section
   - Copy the URI format connection string
   - Replace `[YOUR-PASSWORD]` with your actual password

3. **View Your Data:**
   - Use the Table Editor in Supabase dashboard
   - View your `tasks_task` and `tasks_weatherlog` tables
   - Monitor real-time data changes

## 🚨 Troubleshooting

### Common Issues

1. **Database connection issues**
   - Verify your Supabase DATABASE_URL in `.env`
   - Check if your Supabase project is active
   - Ensure your IP is allowed (Supabase → Settings → Database → Network Restrictions)
   - Test connection: `curl http://localhost:8000/api/debug-config/`

2. **Weather API not working**
   - Check your `WEATHER_API_KEY` in `.env`
   - Verify the API key is valid at OpenWeatherMap
   - Test with: `curl http://localhost:8000/api/debug-config/`

3. **Tasks not saving**
   - Check Supabase database connection
   - Verify migrations were applied: `python manage.py migrate`
   - Check Supabase dashboard → Table Editor for `tasks_task` table
   - Look for errors in browser developer tools

4. **Charts not displaying**
   - Ensure matplotlib is installed: `pip install matplotlib`
   - Check if tasks exist in database

5. **Server not starting**
   - Check if port 8000 is available
   - Verify all dependencies are installed: `pip list`
   - Check `.env` file format and Supabase connection
   - Ensure `psycopg2-binary` is installed for PostgreSQL

### Debug Commands

```bash
# Check system configuration
curl http://localhost:8000/api/debug-config/

# Run Django checks
python manage.py check

# View Django logs
python manage.py runserver --verbosity=2

# Test database connection with Supabase
python manage.py shell
>>> from tasks.models import Task
>>> Task.objects.count()  # Should return number without errors

# Check Supabase connection specifically
python manage.py dbshell  # Should connect to your Supabase database
```

## 📱 Browser Compatibility

- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 🔒 Security Notes

- Never commit your `.env` file to version control
- Generate a unique `SECRET_KEY` using the command provided above
- Use strong, unique `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Configure proper CORS settings for production
- Keep your Supabase database password secure
- Use Supabase Row Level Security (RLS) for production apps

## 💾 Database Management

### Viewing Your Data
- **Supabase Dashboard**: Go to Table Editor to view/edit data
- **Django Admin**: Access at `http://localhost:8000/admin/` (after creating superuser)
- **API Endpoints**: Use the REST API to manage data programmatically

### Backup & Migration
- **Supabase**: Automatic backups available in dashboard
- **Local Backup**: Use `python manage.py dumpdata` for Django fixtures
- **Migration**: Standard Django migrations work with Supabase

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Verify your `.env` configuration
3. Test API endpoints individually
4. Check browser console for JavaScript errors

## 🎯 Future Enhancements

- [ ] User authentication and authorization
- [ ] Task due dates and reminders
- [ ] File attachments for tasks
- [ ] Team collaboration features
- [ ] Advanced filtering and search
- [ ] Task categories and tags
- [ ] Email notifications
- [ ] Mobile app (React Native)

---

**Happy Task Management! 🎉**
