# MongoDB Schema Documentation

## Overview
This document describes the MongoDB schema structure for the Multiple Disease Prediction application. The application uses NestJS with Mongoose for MongoDB integration.

## Database Collections

### 1. Users Collection (`users`)
Stores user authentication and profile information.

**Schema:** `User`
- **Purpose:** User management, authentication, and profile data
- **Key Fields:**
  - `name`: User's full name (required)
  - `email`: Unique email address (required, indexed)
  - `password`: Hashed password (required)
  - `role`: User role (user/admin/doctor)
  - `profileImage`: Profile picture URL
  - `gender`: User's gender
  - `age`: User's age
  - `phoneNumber`: Contact number
  - `address`, `city`, `country`: Location information
  - `isEmailVerified`, `isPhoneVerified`: Verification status
  - `lastLoginAt`: Last login timestamp
  - `isActive`: Account status

**Indexes:**
- `email: 1` (unique)
- `role: 1`
- `createdAt: -1`
- `isActive: 1`

### 2. Chat Messages Collection (`chat_messages`)
Stores conversation history between users and the AI chatbot.

**Schema:** `ChatMessage`
- **Purpose:** Chat history, symptom input, and disease predictions
- **Key Fields:**
  - `sender`: Message sender (user/bot)
  - `messageType`: Type of message (text, symptom_input, disease_prediction, etc.)
  - `content`: Message content
  - `diseases`: Array of disease predictions with confidence scores
  - `symptomInput`: Structured symptom information
  - `userId`: Reference to user
  - `replyTo`: Reference to parent message (for threaded conversations)
  - `replies`: Array of reply message IDs
  - `isRead`, `isArchived`: Message status flags
  - `metadata`: Additional message data

**Indexes:**
- `userId: 1, timestamp: -1`
- `sender: 1, timestamp: -1`
- `messageType: 1, timestamp: -1`
- `isRead: 1, userId: 1`

### 3. Predictions Collection (`predictions`)
Stores disease prediction results and analysis.

**Schema:** `Prediction`
- **Purpose:** Disease prediction results, symptom analysis, and model performance
- **Key Fields:**
  - `symptoms`: User-reported symptoms
  - `diseases`: Array of predicted diseases with details
  - `response`: AI-generated response
  - `userId`: Reference to user
  - `status`: Prediction processing status
  - `accuracy`: Prediction confidence level
  - `symptomAnalysis`: Detailed symptom breakdown
  - `modelPerformance`: Model metrics and version
  - `isFollowUpRequired`: Follow-up flag
  - `followUpDate`: Scheduled follow-up date

**Indexes:**
- `userId: 1, createdAt: -1`
- `status: 1, createdAt: -1`
- `accuracy: 1, createdAt: -1`
- `isFollowUpRequired: 1, followUpDate: 1`
- `tags: 1`

### 4. Diseases Collection (`diseases`)
Stores comprehensive disease information and metadata.

**Schema:** `Disease`
- **Purpose:** Disease database with symptoms, precautions, and treatments
- **Key Fields:**
  - `name`: Disease name (unique)
  - `description`: Detailed disease description
  - `category`: Disease category (infectious, cardiovascular, etc.)
  - `severity`: Disease severity level
  - `symptoms`: Array of associated symptoms with frequency
  - `precautions`: Prevention and safety measures
  - `treatments`: Available treatment options
  - `riskFactors`: Risk factors for the disease
  - `complications`: Potential complications
  - `specialists`: Recommended medical specialists
  - `statistics`: Prevalence, mortality rates, etc.

**Indexes:**
- `name: 1`
- `category: 1, severity: 1`
- `symptoms.name: 1`
- `tags: 1`
- `statistics.prevalence: -1`

### 5. Medical Records Collection (`medical_records`)
Stores comprehensive patient medical history.

**Schema:** `MedicalRecord`
- **Purpose:** Patient medical history, treatments, and health data
- **Key Fields:**
  - `userId`: Reference to user
  - `recordType`: Type of medical record
  - `status`: Record status (active, resolved, etc.)
  - `title`, `description`: Record details
  - `date`: Record date
  - `vitalSigns`: Blood pressure, heart rate, temperature, etc.
  - `medications`: Prescribed medications
  - `labResults`: Laboratory test results
  - `surgeries`: Surgical procedures
  - `allergies`: Known allergies
  - `chronicConditions`: Long-term health conditions
  - `familyHistory`: Family medical history

**Indexes:**
- `userId: 1, date: -1`
- `userId: 1, recordType: 1`
- `userId: 1, status: 1`
- `recordType: 1, date: -1`
- `medications.name: 1`

## Data Relationships

```
User (1) ←→ (Many) ChatMessage
User (1) ←→ (Many) Prediction  
User (1) ←→ (Many) MedicalRecord
ChatMessage (1) ←→ (Many) ChatMessage (replies)
Disease (1) ←→ (Many) Prediction (via diseases array)
```

## Schema Features

### Validation
- **Required Fields:** Essential data validation
- **String Lengths:** Maximum length constraints
- **Enums:** Restricted value sets
- **Custom Validators:** Business logic validation

### Indexing
- **Performance:** Optimized query performance
- **Compound Indexes:** Multi-field queries
- **Text Search:** Full-text search capabilities
- **Geospatial:** Location-based queries (if needed)

### Timestamps
- **Automatic:** Created/updated timestamps
- **Audit Trail:** Data modification tracking
- **Versioning:** Document version management

### Security
- **Password Hashing:** Secure password storage
- **Role-based Access:** User permission levels
- **Data Privacy:** Sensitive data protection

## Usage Examples

### Creating a User
```typescript
const user = new User({
  name: 'John Doe',
  email: 'john@example.com',
  password: 'hashedPassword',
  role: UserRole.USER,
  gender: Gender.MALE,
  age: 30
});
```

### Adding a Chat Message
```typescript
const message = new ChatMessage({
  sender: MessageSender.USER,
  messageType: MessageType.SYMPTOM_INPUT,
  content: 'I have fever and headache',
  userId: user._id,
  symptomInput: {
    symptoms: ['fever', 'headache'],
    severity: 'moderate',
    duration: '2 days'
  }
});
```

### Creating a Prediction
```typescript
const prediction = new Prediction({
  symptoms: 'fever, headache, fatigue',
  diseases: [{
    disease: 'Common Cold',
    confidence: 0.85,
    probability: 0.78,
    symptoms: ['fever', 'headache', 'fatigue'],
    precautions: ['rest', 'fluids', 'medication'],
    severity: 'mild',
    recommendedAction: 'Rest and monitor symptoms',
    urgency: 'routine'
  }],
  response: 'Based on your symptoms, you likely have a common cold...',
  userId: user._id,
  status: PredictionStatus.COMPLETED,
  accuracy: PredictionAccuracy.HIGH
});
```

## Best Practices

1. **Indexing:** Use compound indexes for common query patterns
2. **Validation:** Implement comprehensive data validation
3. **Performance:** Monitor query performance and optimize indexes
4. **Security:** Always hash passwords and validate user input
5. **Scalability:** Design schemas for future growth
6. **Consistency:** Maintain data consistency across collections

## Migration Considerations

When updating schemas:
1. **Backward Compatibility:** Ensure existing data remains accessible
2. **Data Migration:** Plan for data structure changes
3. **Index Updates:** Update indexes for new query patterns
4. **Validation:** Test new validation rules with existing data
5. **Rollback Plan:** Prepare rollback strategy if needed
