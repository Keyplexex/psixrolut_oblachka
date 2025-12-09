# Лабораторная работа №3
## Что мы сделали?
Нашей задачей было написать "плохой" и "хороший" CI/CD файл, в которых описать не менее трех bad practices и как мы их исправили вдальнейшем.

# Часть 1

## "Плохой" CI/CD файл
```
name: Working Bad CI/CD

on:
  push:
    branches: [main]

jobs:
  demonstrate-bad-practices:
    runs-on: ubuntu-22.04
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Install Python (the wrong way)
      run: |
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip python3-venv
        
    - name: Show bad logging
      run: |
        echo "  WARNING: This is a BAD PRACTICE"
        echo "Hardcoded test credentials:"
        echo "  Username: admin"
        echo "  Password: Admin123!"
        echo "  API Key: test_sk_1234567890abcdef"
        
    - name: Run tests (ignoring results)
      run: |
        echo "Running tests..."
        if python -m pytest test_main.py -v; then
          echo "✅ Tests passed"
        else
          echo "❌ Tests failed, but continuing anyway..."
        fi
        
    - name: Deploy simulation
      run: |
        echo " STARTING DEPLOYMENT SIMULATION"
        echo ""
        echo " BAD PRACTICES DEMONSTRATED:"
        echo "1.  Hardcoded secrets in logs"
        echo "2.  No condition checks before deploy"
        echo "3.  Inefficient dependency installation"
        echo "4.  Ignoring test failures"
```

## "Хороший" CI/CD файл
```
name: Good CI/CD (Fixed)

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-22.04
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.10"
        
    - name: Cache pip packages
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
        
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest
        
    - name: Show environment info
      env:
        TEST_MODE: ${{ secrets.TEST_MODE || 'development' }}
      run: |
        echo "Running in $TEST_MODE mode"
        echo "No secrets exposed here"
        
    - name: Run tests
      run: |
        python -m pytest test_main.py -v
        # Если тесты упадут, workflow остановится здесь
        
    - name: Deploy simulation
      if: success()
      run: |
        echo "✅ All tests passed, proceeding with deployment simulation"
        echo "Deployment would happen here..."
```

## Объяснение!
### 1. Работа с секретами
**Плохая практика:❌ Проблема: Секреты в открытом виде в логах. Доступны всем, кто видит логи.
```
echo "Hardcoded test credentials:"
echo "  Username: admin"
echo "  Password: Admin123!"
```

**Хорошая практика:✅ Исправление: Секреты хранятся в GitHub Secrets, не выводятся в логи.
```
env:
  TEST_MODE: ${{ secrets.TEST_MODE || 'development' }}
run: |
  echo "Running in $TEST_MODE mode"
  echo "No secrets exposed here"
```

### 2. Обработка тестов
**Плохая практика:❌ Проблема: Игнорирование результатов тестов. Деплой продолжается даже при падении тестов.
```
if python -m pytest test_main.py -v; then
  echo "✅ Tests passed"
else
  echo "❌ Tests failed, but continuing anyway..."
fi
```

**Хорошая практика:✅ Исправление: Если тесты упадут, команда вернет ненулевой код выхода и workflow остановится.
```
run: |
  python -m pytest test_main.py -v
```


### 3. Установка зависимостей

**Плохая практика:❌ Проблема: Установка с нуля каждый раз, без кеширования, медленно.
```
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv
```
**Хорошая практика:✅ Исправление: Использование готовых действий и кеширование.
```
- uses: actions/setup-python@v4
  with:
    python-version: "3.10"
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

### 4. Управление деплоем

**Плохая практика:❌ Проблема: Деплой всегда выполняется, нет условий.
```
- name: Deploy simulation
  run: |
    echo "🚀 STARTING DEPLOYMENT SIMULATION"
```
**Хорошая практика:✅ Исправление: Деплой только при успешном выполнении всех предыдущих шагов.
```
- name: Deploy simulation
  if: success()
  run: |
    echo "✅ All tests passed, proceeding with deployment"
```

### Пайплайн "плохого" CI/CD:
![omg](jiraf/bad.png)

### Пайплайн "хорошего" CI/CD:
![omg](jiraf/god.png)
# Выводы: ключевые улучшения CI/CD

## 📈 Основные изменения

| Аспект | Было | Стало | Эффект |
|--------|------|-------|---------|
| ** Безопасность** | Секреты в логах | GitHub Secrets | Защита данных |
| ** Надежность** | Игнорирование тестов | Тесты блокируют деплой | Качество кода |
| ** Эффективность** | Установка с нуля | Кеширование | Быстрее на 60-70% |
| ** Контроль** | Автодеплой | Условный деплой | Управляемость |

##  Итоговый результат

1. **Безопасность ** - данные защищены, секреты не утекают
2. **Надежность ** - в production попадает только проверенный код  
3. **Скорость ** - кеширование ускоряет выполнение
4. **Управление ** - полный контроль над процессом деплоя
![omg](jiraf/photo_5314528619122069628_y.jpg)
