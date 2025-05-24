# 🛂 Авторизация и Регистрация API

## 🛡️ JWT Защищенные роуты

Все защищённые роуты требуют в заголовке:

```
Authorization: Bearer <jwt_token>
```

---

# 👤 Профиль пользователя (FastAPI)

## 🧾 1. Получить информацию о пользователе

**GET** `/api/v1/profile`

### 🔐 Role: User (авторизованный)

**Описание:**  
Получает полную информацию о себе для отображения в профиле на фронте.

**Примечание:**  
- Имя (`name`) и почта (`email`) сохраняются в БД при регистрации на фронтенде.  
- При запросе `/profile` данные извлекаются из БД по `userId`, который содержится в JWT токене.  
- Остальные поля (`surname`, `phone`, `bio` и т.д.) будут `null` или пустыми, пока пользователь сам не заполнит их через `PATCH /profile`.

### ✅ Response JSON:
```json
{
  "userId": "1",
  "name": "Diyar",
  "surname": "Amangeldi",
  "email": "diyar@gmail.com",
  "gender": "male",
  "birth_date": "2002-04-05",
  "phone": "+77001234567",
  "nationality": "Kazakh",
  "country": "Kazakhstan",
  "city": "Astana",
  "bio": "I’m a 3rd year student at AITU.",
  "university": "Astana IT University",
  "student_id_number": "AITU-123456",
  "group": "SE-2202",
  "roommate_preferences": "non-smoker, quiet",
  "language_preferences": ["Kazakh", "Russian", "English"],
  "budget_range": {
    "min": 50000,
    "max": 90000
  },
  "avatar_url": "https://cdn.domain.com/avatar.jpg", // File 
  "id_document_url": "https://cdn.domain.com/id.png", // File
  // мб еще хз добавишь что то но эти поля сверху чутька я буду там загружать File
  "document_verified": true,
  "social_links": {
    "telegram": "@diyar",
  },
  "created_at": "2025-03-01T12:00:00Z",
  "last_login": "2025-04-21T09:00:00Z"
}
```

---

## 🆕 2. Создать профиль пользователя

**POST** `/api/v1/profile`

### 🔐 Role: User (авторизованный)

**Описание:**  
Создаёт или заполняет профиль пользователя после регистрации, если такой ещё не существует. Это полезно, если регистрация через соцсети (например, Google OAuth2), и вы хотите потом до-заполнить информацию.

### 📥 Пример запроса:
```json
{
  "name": "Diyar",
  "surname": "Amangeldi",
  "gender": "male",
  "birth_date": "2002-04-05",
  "email": "diyar@gmail.com",
  "phone": "+77001234567",
  "nationality": "Kazakh",
  "country": "Kazakhstan",
  "city": "Astana",
  "bio": "Web developer & AITU student",
  "university": "Astana IT University",
  "student_id_number": "AITU-123456",
  "group": "se-2202",
  "roommate_preferences": "non-smoker",
  "language_preferences": ["Kazakh", "English"],
  "budget_range": {
    "min": 50000,
    "max": 90000
  },
  "avatar_url": "https://cdn.domain.com/avatar.jpg",
  "id_document_url": "https://cdn.domain.com/id-card.png",
  "social_links": {
    "telegram": "@diyar_dev",
  }
}
```

### ✅ Response JSON:
```json
{
  "message": "Profile created successfully.",
  "userId": "1"
}
```

**⚠️ Условия:**  
- Если профиль уже существует, возвращается ошибка или выполняется редирект на `PATCH /profile` (в зависимости от логики).  
- Нужно обязательно быть авторизованным (JWT).

---

## ✏️ 3. Обновить профиль пользователя

**PATCH** `/api/v1/profile`

### 🔐 Role: User

**Описание:**  
Обновляет любые поля профиля пользователя.

### 🔸 Request JSON (можно отправлять частично):
```json
{
  "name": "Diyar",
  "surname": "Amangeldi",
  "email": "diyar@gmail.com",
  "gender": "male",
  "birth_date": "2002-04-05",
  "phone": "+77001234567",
  "nationality": "Kazakh",
  "country": "Kazakhstan",
  "city": "Astana",
  "bio": "I’m a 3rd year student at AITU.",
  "university": "Astana IT University",
  "student_id_number": "AITU-123456",
  "group": "SE-2202",
  "roommate_preferences": "non-smoker, quiet",
  "language_preferences": ["Kazakh", "Russian", "English"],
  "budget_range": {
    "min": 50000,
    "max": 90000
  },
  "avatar_url": "https://cdn.domain.com/avatar.jpg",
  "id_document_url": "https://cdn.domain.com/id.png",
  "document_verified": true,
  "social_links": {
    "telegram": "@diyar",
  }
}
```

### ✅ Response JSON:
```json
{
  "message": "Profile updated successfully."
}
```

---

## 🔐 JWT Защита

Для всех роутов обязателен токен:

```
Authorization: Bearer <jwt_token>
```

---

# 📚 Документация API (FastAPI)

## 🏠 Публикация квартиры

### 🏗️ 1. Публикация квартиры

**POST** `/api/v1/my-apartments`

#### 🔐 Role: User (Student / Landlord)

**Описание:**  
Студент публикует квартиру, которая сразу становится доступной для бронирования.

#### 🔸 Request JSON:
```json
[
  {
    "apartment_id": "1",
    "apartment_name": "Студенческий уют AITU",
    "description": "Сдаётся светлая квартира рядом с университетом. Отлично подойдёт для студентов.",
    
    "address": {
      "street": "ул. Кабанбай батыра",
      "house_number": "10",
      "apartment_number": "12",
      "entrance": "2",
      "has_intercom": true,
      "landmark": "рядом с Burger King",
    },

    "district_name": "Yesil",
    "latitude": 51.0909,
    "longitude": 71.4187,

    "price_per_month": 95000,
    "area": 50.0,
    "kitchen_area": 8.0,
    "floor": 5,
    "number_of_rooms": 2,
    "max_users": 2,

    "available_from": "2025-05-01",
    "available_until": "2025-08-31",

    "university_nearby": "Astana IT University",

    "pictures": [
      "https://cdn.domain.com/img1.jpg",
      "https://cdn.domain.com/img2.jpg"
    ],

    "is_promoted": false,
    "is_pet_allowed": true,

    "rental_type": "room",
    "roommate_preferences": "не шумные, девушки, без животных",
    "included_utilities": ["Wi-Fi", "вода", "мебель", "стиральная машина"],
    "rules": ["только девушкам", "нельзя курить"],

    "contact_phone": "+77001234567",
    "contact_telegram": "@aitu_host"
  }
]


```

#### ✅ Response JSON:
```json
{
  "message": "Apartment published with map location.",
  "apartment_id": "a12345"
}
```

---

### 🏠 2. Просмотр всех своих квартир

**GET** `/api/v1/my-apartments`

#### 🔐 Role: User

**Описание:**  
Получить список всех квартир, которые ты опубликовал.

#### ✅ Response JSON:
```json
{
  "apartments": [
    {
      "apartment_id": "1",
    },
    {
      "apartment_id": "2",
    }
  ]
}
```

---

### 🧾 3. Просмотр заявок на свою квартиру

**GET** `/api/v1/my-apartments/:id/bookings`

#### 🔐 Role: User

**Описание:**  
Список бронирований твоей квартиры, с сообщениями и профилями арендаторов.

#### ✅ Response JSON:
```json
{
  "bookings": [
    {
      "booking_id": "b102",
      "user": {
        "userId": "1",
        "name": "Andreas",
        "avatar_url": "https://cdn.domain.com/u334.jpg",
        "university": "AITU",
        "email": "andreas@mail.com"
      },
      "message": "I'm a 3rd year student at AITU, looking for a room from September to December. I’m tidy and respectful.",
      "application_date": "2023-12-09",
      "status": "pending"
    }
  ]
}
```

---

### ✅❌ 4. Принять или отклонить заявку

**PATCH** `/api/v1/my-apartments/:apartment_id/bookings/:booking_id`

#### 🔐 Role: User

**Описание:**  
Принять или отклонить бронь от студента.

#### 🔸 Request JSON:
```json
{
  "status": "accepted" // или rejected, или pending
}
```

#### ✅ Response JSON:
```json
{
  "message": "Booking status updated."
}
```

---

### 🧾 5. Получение списка квартир, где ты подал заявку

**GET** `/api/v1/my-bookings`

#### 🔐 Role: User

**Описание:**  
Посмотреть, на какие квартиры ты подавал заявку.

#### ✅ Response JSON:
```json
{
  "applications": [
    {
      "apartment_id": "2",
      "apartment_name": "Parque Eduardo VII",
      "price": 50000,
      "name": "Dastan",
      "application_date": "2023-12-09",
      "status": "waiting_approval"
    }
  ]
}
```

---

## 🧾 6. Верификация арендодателей

**POST** `/api/v1/landlords/verify`

### 🔐 Role: Admin

**Описание:**  
Позволяет администратору верифицировать арендодателя, проверяя его документы и подтверждая его статус.

### 🔸 Request JSON:
```json
{
  "landlord_id": "u12345",
  "verification_documents": [
    "https://cdn.domain.com/doc1.jpg",
    "https://cdn.domain.com/doc2.jpg"
  ]
}
```

### ✅ Response JSON:
```json
{
  "message": "Landlord verified successfully.",
  "landlord_id": "u12345",
  "verified": true
}
```

---

## 💳 7. Безопасные платежи

**POST** `/api/v1/payments`

### 🔐 Role: User

**Описание:**  
Обеспечивает безопасные платежи для бронирования квартир.

### 🔸 Request JSON:
```json
{
  "booking_id": "b102",
  "amount": 95000,
  "payment_method": "credit_card",
  "card_details": {
    "card_number": "4111111111111111",
    "expiry_date": "12/25",
    "cvv": "123"
  }
}
```

### ✅ Response JSON:
```json
{
  "message": "Payment processed successfully.",
  "payment_id": "p56789",
  "status": "completed"
}
```

---

## 🌟 8. Система отзывов и рейтингов

**POST** `/api/v1/reviews`

### 🔐 Role: User

**Описание:**  
Позволяет пользователям оставлять отзывы и рейтинги для арендодателей или квартир.

### 🔸 Request JSON:
```json
{
  "target_id": "u12345", // ID арендодателя или квартиры
  "rating": 4,
  "text": "Отличный опыт аренды, всё прошло гладко!"
}
```

### ✅ Response JSON:
```json
{
  "message": "Review submitted successfully.",
  "review_id": "r78901"
}
```

---

## 💬 9. Чат с арендодателями

**POST** `/api/v1/chats`

### 🔐 Role: User

**Описание:**  
Создаёт чат между пользователем и арендодателем.

### 🔸 Request JSON:
```json
{
  "landlord_id": "u12345",
  "message": "Здравствуйте, квартира ещё доступна?"
}
```

### ✅ Response JSON:
```json
{
  "chat_id": "c45678",
  "message": "Chat created successfully."
}
```

**GET** `/api/v1/chats/:chat_id`

### 🔐 Role: User

**Описание:**  
Получает историю сообщений в чате.

### ✅ Response JSON:
```json
{
  "chat_id": "c45678",
  "messages": [
    {
      "sender": "user",
      "text": "Здравствуйте, квартира ещё доступна?",
      "timestamp": "2025-04-21T09:00:00Z"
    },
    {
      "sender": "landlord",
      "text": "Да, доступна.",
      "timestamp": "2025-04-21T09:05:00Z"
    }
  ]
}
```

---

## 🗺️ 10. Интерактивная карта

**GET** `/api/v1/map`

### 🔐 Role: User

**Описание:**  
Возвращает данные для отображения квартир на интерактивной карте.

### ✅ Response JSON:
```json
{
  "apartments": [
    {
      "apartment_id": "a12345",
      "latitude": 51.0909,
      "longitude": 71.4187,
      "price_per_month": 95000,
      "apartment_name": "Студенческий уют AITU"
    },
    {
      "apartment_id": "a12346",
      "latitude": 51.1200,
      "longitude": 71.4500,
      "price_per_month": 85000,
      "apartment_name": "Квартира рядом с университетом"
    }
  ]
}
```

---

## 🛠️ Дополнительные улучшения

### 11. Уведомления о новых квартирах

**POST** `/api/v1/notifications/subscribe`

### 🔐 Role: User

**Описание:**  
Позволяет пользователю подписаться на уведомления о новых квартирах.

### 🔸 Request JSON:
```json
{
  "filters": {
    "price_range": {
      "min": 50000,
      "max": 100000
    },
    "location": "Astana",
    "room_type": "shared"
  }
}
```

### ✅ Response JSON:
```json
{
  "message": "Subscription created successfully.",
  "subscription_id": "s12345"
}
```

---

### 12. Поиск соседей по интересам

**POST** `/api/v1/roommates`

### 🔐 Role: User

**Описание:**  
Позволяет пользователям находить соседей по интересам.

### 🔸 Request JSON:
```json
{
  "preferences": {
    "gender": "male",
    "smoking": false,
    "languages": ["English", "Kazakh"]
  }
}
```

### ✅ Response JSON:
```json
{
  "roommates": [
    {
      "userId": "u56789",
      "name": "Dastan",
      "bio": "Студент AITU, люблю тишину и порядок.",
      "languages": ["English", "Kazakh"]
    }
  ]
}
```
