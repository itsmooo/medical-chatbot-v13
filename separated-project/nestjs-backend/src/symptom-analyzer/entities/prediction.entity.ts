import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document, Schema as MongooseSchema, Types } from 'mongoose';
import { User } from '../../auth/entities/user.entity';

export enum PredictionStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed'
}

export enum PredictionAccuracy {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high'
}

export interface DiseaseResult {
  disease: string;
  confidence: number;
  probability: number;
  symptoms: string[];
  precautions: string[];
  severity: 'low' | 'medium' | 'high';
  recommendedAction: string;
  specialist?: string;
  urgency: 'routine' | 'soon' | 'urgent' | 'emergency';
}

export interface SymptomAnalysis {
  primarySymptoms: string[];
  secondarySymptoms: string[];
  severity: 'mild' | 'moderate' | 'severe';
  duration: string;
  frequency: string;
  triggers?: string[];
  alleviators?: string[];
}

export interface ModelPerformance {
  modelName: string;
  confidence: number;
  accuracy: number;
  processingTime: number;
  version: string;
}

export type PredictionDocument = Prediction & Document;

@Schema({ 
  timestamps: true,
  collection: 'predictions'
})
export class Prediction {
  @Prop({ 
    required: true,
    trim: true,
    maxlength: 1000
  })
  symptoms: string;

  @Prop({ 
    type: [Object], 
    default: [],
    validate: {
      validator: function(diseases: any[]) {
        return diseases.length <= 20; // Max 20 diseases per prediction
      },
      message: 'Cannot have more than 20 diseases per prediction'
    }
  })
  diseases: DiseaseResult[];

  @Prop({ 
    required: true,
    trim: true,
    maxlength: 2000
  })
  response: string;

  @Prop({ 
    type: MongooseSchema.Types.ObjectId, 
    ref: 'User', 
    required: true,
    index: true
  })
  userId: Types.ObjectId;

  @Prop({
    type: String,
    enum: Object.values(PredictionStatus),
    default: PredictionStatus.PENDING,
    index: true
  })
  status: PredictionStatus;

  @Prop({
    type: String,
    enum: Object.values(PredictionAccuracy),
    default: PredictionAccuracy.MEDIUM
  })
  accuracy: PredictionAccuracy;

  @Prop({ 
    type: Object,
    default: null
  })
  symptomAnalysis?: SymptomAnalysis;

  @Prop({ 
    type: Object,
    default: null
  })
  modelPerformance?: ModelPerformance;

  @Prop({ 
    type: [String],
    default: []
  })
  tags: string[];

  @Prop({ 
    default: false
  })
  isFollowUpRequired: boolean;

  @Prop({ 
    type: Date,
    default: null
  })
  followUpDate?: Date;

  @Prop({ 
    type: String,
    default: null
  })
  followUpNotes?: string;

  @Prop({ 
    type: Object,
    default: {}
  })
  metadata?: Record<string, any>;

  @Prop()
  createdAt: Date;

  @Prop()
  updatedAt: Date;
}

export const PredictionSchema = SchemaFactory.createForClass(Prediction);

// Add indexes for better query performance
PredictionSchema.index({ userId: 1, createdAt: -1 });
PredictionSchema.index({ status: 1, createdAt: -1 });
PredictionSchema.index({ accuracy: 1, createdAt: -1 });
PredictionSchema.index({ isFollowUpRequired: 1, followUpDate: 1 });
PredictionSchema.index({ tags: 1 });
PredictionSchema.index({ 'diseases.disease': 1 });
PredictionSchema.index({ 'diseases.severity': 1 });
PredictionSchema.index({ 'diseases.urgency': 1 });
