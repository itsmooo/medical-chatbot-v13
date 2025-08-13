import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document, Schema as MongooseSchema, Types } from 'mongoose';
import { User } from '../../auth/entities/user.entity';

export enum MessageSender {
  USER = 'user',
  BOT = 'bot',
}

export enum MessageType {
  TEXT = 'text',
  SYMPTOM_INPUT = 'symptom_input',
  DISEASE_PREDICTION = 'disease_prediction',
  FOLLOW_UP = 'follow_up',
  ERROR = 'error'
}

export interface DiseasePrediction {
  disease: string;
  confidence: number;
  symptoms: string[];
  precautions?: string[];
  severity?: 'low' | 'medium' | 'high';
  recommendedAction?: string;
}

export interface SymptomInput {
  symptoms: string[];
  severity: 'mild' | 'moderate' | 'severe';
  duration?: string;
  additionalNotes?: string;
}

export type ChatMessageDocument = ChatMessage & Document;

@Schema({ 
  timestamps: { createdAt: 'timestamp', updatedAt: 'updatedAt' },
  collection: 'chat_messages'
})
export class ChatMessage {
  @Prop({
    type: String,
    enum: Object.values(MessageSender),
    required: true,
    index: true
  })
  sender: MessageSender;

  @Prop({
    type: String,
    enum: Object.values(MessageType),
    default: MessageType.TEXT,
    index: true
  })
  messageType: MessageType;

  @Prop({ 
    required: true,
    trim: true,
    maxlength: 2000
  })
  content: string;

  @Prop({ 
    type: [Object], 
    default: [],
    validate: {
      validator: function(diseases: any[]) {
        return diseases.length <= 10; // Max 10 diseases per message
      },
      message: 'Cannot have more than 10 diseases per message'
    }
  })
  diseases: DiseasePrediction[];

  @Prop({ 
    type: Object,
    default: null
  })
  symptomInput?: SymptomInput;

  @Prop({ 
    type: MongooseSchema.Types.ObjectId, 
    ref: 'User', 
    required: true,
    index: true
  })
  userId: Types.ObjectId;

  @Prop({ 
    type: MongooseSchema.Types.ObjectId, 
    ref: 'ChatMessage',
    default: null
  })
  replyTo?: Types.ObjectId;

  @Prop({ 
    type: [MongooseSchema.Types.ObjectId], 
    ref: 'ChatMessage',
    default: []
  })
  replies: Types.ObjectId[];

  @Prop({ 
    default: false
  })
  isRead: boolean;

  @Prop({ 
    default: false
  })
  isArchived: boolean;

  @Prop()
  timestamp: Date;

  @Prop()
  updatedAt: Date;

  @Prop({ 
    type: Object,
    default: {}
  })
  metadata?: Record<string, any>;
}

export const ChatMessageSchema = SchemaFactory.createForClass(ChatMessage);

// Add indexes for better query performance
ChatMessageSchema.index({ userId: 1, timestamp: -1 });
ChatMessageSchema.index({ sender: 1, timestamp: -1 });
ChatMessageSchema.index({ messageType: 1, timestamp: -1 });
ChatMessageSchema.index({ isRead: 1, userId: 1 });
ChatMessageSchema.index({ isArchived: 1, userId: 1 });
