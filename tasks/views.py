import requests
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Q
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from decouple import config
from .models import Task, WeatherLog
from .serializers import TaskSerializer, WeatherLogSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        queryset = Task.objects.all()
        status_filter = self.request.query_params.get('status', None)
        priority_filter = self.request.query_params.get('priority', None)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
            
        return queryset

@api_view(['GET'])
def test_endpoint(request):
    """Simple test endpoint to verify URL routing works"""
    return Response({
        'status': 'success',
        'message': 'URL routing is working!',
        'available_endpoints': [
            '/api/tasks/',
            '/api/weather/<city>/',
            '/api/analytics/',
            '/api/test/',
        ],
        'request_method': request.method,
        'request_path': request.path,
        'timestamp': timezone.now().isoformat(),
    })

@api_view(['GET'])
def get_weather(request, city):
    """Get weather data from OpenWeatherMap API and store it"""
    print(f"=== Weather API Debug Info ===")
    print(f"Weather endpoint called with city: {city}")
    print(f"Request method: {request.method}")
    print(f"Request path: {request.path}")
    
    # Check if API key is configured
    try:
        api_key = config('WEATHER_API_KEY')
        print(f"API key loaded: {bool(api_key)}")
        if not api_key:
            return Response({
                'error': 'Weather API key not configured',
                'debug_info': 'WEATHER_API_KEY environment variable is empty or not set'
            }, status=500)
    except Exception as e:
        print(f"Error loading API key: {e}")
        return Response({
            'error': 'Weather API key not configured', 
            'debug_info': str(e)
        }, status=500)
    
    # Construct API URL
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    print(f"Making request to OpenWeatherMap API...")
    print(f"City parameter: {city}")
    
    try:
        # Make request to OpenWeatherMap API
        response = requests.get(url, timeout=10)
        print(f"Weather API response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Weather API response data keys: {list(data.keys())}")
            
            # Store weather data in database
            try:
                weather_log = WeatherLog.objects.create(
                    city=data['name'],
                    temperature=data['main']['temp'],
                    description=data['weather'][0]['description'],
                    humidity=data['main']['humidity']
                )
                print(f"Weather data stored in database with ID: {weather_log.id}")
                
                response_data = {
                    'city': data['name'],
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'humidity': data['main']['humidity'],
                    'logged_at': weather_log.timestamp.isoformat(),  # ISO format for JavaScript
                    'logged_at_readable': weather_log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),  # Human readable
                    'feels_like': data['main'].get('feels_like'),
                    'pressure': data['main'].get('pressure'),
                    'visibility': data.get('visibility'),
                    'wind_speed': data.get('wind', {}).get('speed'),
                    'country': data.get('sys', {}).get('country'),
                    'debug_info': {
                        'api_status': 'success',
                        'stored_in_db': True,
                        'timestamp_iso': weather_log.timestamp.isoformat(),
                        'timestamp_unix': int(weather_log.timestamp.timestamp())
                    }
                }
                
            except Exception as db_error:
                print(f"Error storing in database: {db_error}")
                # Continue without storing if DB error occurs
                current_time = timezone.now()
                response_data = {
                    'city': data['name'],
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'humidity': data['main']['humidity'],
                    'logged_at': current_time.isoformat(),
                    'logged_at_readable': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'feels_like': data['main'].get('feels_like'),
                    'pressure': data['main'].get('pressure'),
                    'visibility': data.get('visibility'),
                    'wind_speed': data.get('wind', {}).get('speed'),
                    'country': data.get('sys', {}).get('country'),
                    'debug_info': {
                        'api_status': 'success',
                        'stored_in_db': False,
                        'db_error': str(db_error),
                        'timestamp_iso': current_time.isoformat()
                    }
                }
            
            print(f"Returning successful weather data for {data['name']}")
            return Response(response_data)
            
        elif response.status_code == 401:
            print("Invalid API key")
            return Response({
                'error': 'Invalid weather API key',
                'debug_info': 'Check your WEATHER_API_KEY in .env file'
            }, status=401)
            
        elif response.status_code == 404:
            print(f"City '{city}' not found")
            return Response({
                'error': f"City '{city}' not found",
                'debug_info': 'Try using the exact city name (e.g., "Mumbai" instead of "mumbai")',
                'suggestions': ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Pune']
            }, status=404)
            
        else:
            print(f"Unexpected API response: {response.status_code}")
            return Response({
                'error': f'Weather API returned status {response.status_code}',
                'debug_info': response.text[:200] if response.text else 'No response content',
            }, status=response.status_code)
    
    except requests.exceptions.Timeout:
        print("Request to weather API timed out")
        return Response({
            'error': 'Weather API request timed out',
            'debug_info': 'The weather service is taking too long to respond'
        }, status=504)
        
    except requests.exceptions.ConnectionError:
        print("Connection error to weather API")
        return Response({
            'error': 'Cannot connect to weather API',
            'debug_info': 'Check your internet connection'
        }, status=503)
        
    except Exception as e:
        print(f"Unexpected exception in weather API: {e}")
        return Response({
            'error': 'Unexpected error occurred',
            'debug_info': str(e)
        }, status=500)

@api_view(['GET'])
def task_analytics(request):
    """Generate task analytics and visualization"""
    print("=== Analytics Endpoint Called ===")
    
    try:
        # Get task statistics
        total_tasks = Task.objects.count()
        completed_tasks = Task.objects.filter(status='completed').count()
        pending_tasks = Task.objects.filter(status='pending').count()
        in_progress_tasks = Task.objects.filter(status='in_progress').count()
        
        print(f"Task counts - Total: {total_tasks}, Completed: {completed_tasks}, Pending: {pending_tasks}, In Progress: {in_progress_tasks}")
        
        # Priority distribution
        priority_stats = Task.objects.values('priority').annotate(count=Count('priority'))
        print(f"Priority stats: {list(priority_stats)}")
        
        # Recent tasks
        recent_tasks = Task.objects.order_by('-created_at')[:5]
        recent_tasks_data = [{
            'id': task.id,
            'title': task.title,
            'status': task.status,
            'priority': task.priority,
            'created_at': task.created_at.isoformat(),
        } for task in recent_tasks]
        
        # Create visualization only if we have tasks
        chart_image = None
        if total_tasks > 0:
            try:
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
                
                # Status distribution pie chart
                status_labels = ['Completed', 'Pending', 'In Progress']
                status_data = [completed_tasks, pending_tasks, in_progress_tasks]
                
                # Only show non-zero data
                non_zero_data = [(label, data) for label, data in zip(status_labels, status_data) if data > 0]
                if non_zero_data:
                    labels, chart_data = zip(*non_zero_data)
                    colors = ['#4CAF50', '#FF9800', '#2196F3'][:len(labels)]
                    ax1.pie(chart_data, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
                else:
                    ax1.text(0.5, 0.5, 'No tasks yet', ha='center', va='center', transform=ax1.transAxes)
                ax1.set_title('Task Status Distribution')
                
                # Priority distribution bar chart
                if priority_stats:
                    priorities = [item['priority'] for item in priority_stats]
                    counts = [item['count'] for item in priority_stats]
                    colors = {'low': '#4CAF50', 'medium': '#FF9800', 'high': '#F44336'}
                    bar_colors = [colors.get(p, '#607D8B') for p in priorities]
                    ax2.bar(priorities, counts, color=bar_colors)
                    ax2.set_ylabel('Number of Tasks')
                    ax2.set_xlabel('Priority Level')
                else:
                    ax2.text(0.5, 0.5, 'No tasks yet', ha='center', va='center', transform=ax2.transAxes)
                ax2.set_title('Task Priority Distribution')
                
                plt.tight_layout()
                
                # Convert plot to base64 string
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
                buffer.seek(0)
                image_png = buffer.getvalue()
                buffer.close()
                
                chart_image = base64.b64encode(image_png).decode('utf-8')
                plt.close()
                print("Chart generated successfully")
                
            except Exception as chart_error:
                print(f"Error generating chart: {chart_error}")
                chart_image = None
        else:
            print("No chart generated - no tasks in database")
        
        response_data = {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'in_progress_tasks': in_progress_tasks,
            'completion_rate': round((completed_tasks / total_tasks * 100), 2) if total_tasks > 0 else 0,
            'priority_distribution': list(priority_stats),
            'recent_tasks': recent_tasks_data,
            'chart_image': chart_image,
            'generated_at': timezone.now().isoformat(),
            'debug_info': {
                'chart_generated': chart_image is not None,
                'has_tasks': total_tasks > 0,
                'recent_tasks_count': len(recent_tasks_data)
            }
        }
        
        print("Analytics response prepared successfully")
        return Response(response_data)
        
    except Exception as e:
        print(f"Error in task_analytics: {e}")
        return Response({
            'error': 'Failed to generate analytics',
            'debug_info': str(e)
        }, status=500)

def dashboard(request):
    """Render the dashboard template"""
    print(f"=== Dashboard View Called ===")
    print(f"Request method: {request.method}")
    print(f"Request path: {request.path}")
    
    try:
        # Get some basic stats to pass to template
        task_count = Task.objects.count()
        recent_tasks = Task.objects.order_by('-created_at')[:5]
        completed_tasks = Task.objects.filter(status='completed').count()
        pending_tasks = Task.objects.filter(status='pending').count()
        
        context = {
            'task_count': task_count,
            'recent_tasks': recent_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
        }
        
        print(f"Dashboard context: task_count={task_count}")
        return render(request, 'dashboard.html', context)
        
    except Exception as e:
        print(f"Error in dashboard view: {e}")
        # Return a simple HTTP response if template rendering fails
        return HttpResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Task Manager Dashboard</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .endpoint {{ background: #f5f5f5; padding: 10px; margin: 5px 0; border-radius: 5px; }}
                .error {{ color: #d32f2f; background: #ffebee; padding: 10px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h1>🚀 Task Manager Dashboard</h1>
            <div class="error">
                <strong>Template Error:</strong> {e}
            </div>
            <h2>Available API Endpoints:</h2>
            <div class="endpoint"><a href="/api/tasks/" target="_blank">📋 /api/tasks/ - Task Management</a></div>
            <div class="endpoint"><a href="/api/weather/Mumbai/" target="_blank">🌦️ /api/weather/Mumbai/ - Weather Data</a></div>
            <div class="endpoint"><a href="/api/analytics/" target="_blank">📊 /api/analytics/ - Task Analytics</a></div>
            <div class="endpoint"><a href="/api/test/" target="_blank">🧪 /api/test/ - Test Endpoint</a></div>
            <div class="endpoint"><a href="/api/debug-config/" target="_blank">🔧 /api/debug-config/ - Configuration Debug</a></div>
            
            <h2>Quick Test:</h2>
            <p>Your Django server is running correctly! All API endpoints should be working.</p>
        </body>
        </html>
        """)

@api_view(['GET'])
def debug_config(request):
    """Debug endpoint to check configuration"""
    try:
        # Check environment variables
        env_vars = {}
        try:
            weather_key = config('WEATHER_API_KEY', default='')
            env_vars['weather_api_key_configured'] = bool(weather_key)
            env_vars['weather_api_key_length'] = len(weather_key) if weather_key else 0
        except:
            env_vars['weather_api_key_configured'] = False
            env_vars['weather_api_key_length'] = 0
            
        try:
            env_vars['debug_mode'] = config('DEBUG', default=False, cast=bool)
        except:
            env_vars['debug_mode'] = 'unknown'
        
        # Check database connection
        try:
            task_count = Task.objects.count()
            weather_count = WeatherLog.objects.count()
            db_status = 'connected'
        except Exception as e:
            task_count = 'error'
            weather_count = 'error'
            db_status = f'error: {str(e)}'
        
        # Check recent weather logs
        recent_weather = []
        try:
            recent_logs = WeatherLog.objects.order_by('-timestamp')[:3]
            recent_weather = [{
                'city': log.city,
                'temperature': log.temperature,
                'timestamp': log.timestamp.isoformat(),
            } for log in recent_logs]
        except Exception as e:
            recent_weather = [{'error': str(e)}]
        
        return Response({
            'server_status': 'running',
            'timestamp': timezone.now().isoformat(),
            'environment_variables': env_vars,
            'database': {
                'status': db_status,
                'task_count': task_count,
                'weather_log_count': weather_count,
            },
            'recent_weather_logs': recent_weather,
            'request_info': {
                'method': request.method,
                'path': request.path,
                'user_agent': request.META.get('HTTP_USER_AGENT', 'unknown'),
                'remote_addr': request.META.get('REMOTE_ADDR', 'unknown'),
            },
            'django_info': {
                'timezone': str(timezone.get_current_timezone()),
                'debug_mode': env_vars.get('debug_mode'),
            }
        })
        
    except Exception as e:
        return Response({
            'error': 'Debug endpoint failed',
            'details': str(e),
            'timestamp': timezone.now().isoformat(),
        }, status=500)