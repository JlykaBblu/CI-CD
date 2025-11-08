import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Мокаем БД перед импортом приложения
with patch('pymysql.connect') as mock_connect:
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [0]
    
    from app.app import app

@pytest.fixture
def client():
    return app.test_client()

def test_index_route(client):
    """Тест главной страницы"""
    with patch('app.app.get_db_connection') as mock_db:
        mock_conn = MagicMock()
        mock_db.return_value = mock_conn
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        
        # Мокаем данные из БД
        mock_cursor.fetchall.return_value = [
            {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
            {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'}
        ]
        
        response = client.get('/')
        
        assert response.status_code == 200
        assert 'Данные из БД' in response.get_data(as_text=True)
        assert 'Alice' in response.get_data(as_text=True)
        assert 'Bob' in response.get_data(as_text=True)

def test_db_connection():
    """Тест подключения к БД"""
    with patch('pymysql.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        from app.app import get_db_connection
        
        connection = get_db_connection()
        
        # Проверяем что функция возвращает соединение
        assert connection == mock_conn
        # Проверяем что connect был вызван
        assert mock_connect.called