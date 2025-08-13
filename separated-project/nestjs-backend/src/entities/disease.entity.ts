import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document } from 'mongoose';

export enum DiseaseCategory {
  INFECTIOUS = 'infectious',
  CARDIOVASCULAR = 'cardiovascular',
  RESPIRATORY = 'respiratory',
  NEUROLOGICAL = 'neurological',
  ENDOCRINE = 'endocrine',
  GASTROINTESTINAL = 'gastrointestinal',
  MUSCULOSKELETAL = 'musculoskeletal',
  DERMATOLOGICAL = 'dermatological',
  PSYCHIATRIC = 'psychiatric',
  ONCOLOGICAL = 'oncological',
  OTHER = 'other'
}

export enum DiseaseSeverity {
  MILD = 'mild',
  MODERATE = 'moderate',
  SEVERE = 'severe',
  CRITICAL = 'critical'
}

export interface Symptom {
  name: string;
  description: string;
  frequency: number; // How common this symptom is for this disease (0-1)
  severity: 'mild' | 'moderate' | 'severe';
}

export interface Precaution {
  title: string;
  description: string;
  category: 'lifestyle' | 'medication' | 'environmental' | 'dietary';
  priority: 'low' | 'medium' | 'high';
}

export interface Treatment {
  name: string;
  description: string;
  type: 'medication' | 'surgery' | 'therapy' | 'lifestyle';
  effectiveness: number; // 0-1
  sideEffects?: string[];
}

export type DiseaseDocument = Disease & Document;

@Schema({ 
  timestamps: true,
  collection: 'diseases'
})
export class Disease {
  @Prop({ 
    required: true,
    unique: true,
    trim: true,
    maxlength: 100
  })
  name: string;

  @Prop({ 
    required: true,
    trim: true,
    maxlength: 1000
  })
  description: string;

  @Prop({
    type: String,
    enum: Object.values(DiseaseCategory),
    required: true,
    index: true
  })
  category: DiseaseCategory;

  @Prop({
    type: String,
    enum: Object.values(DiseaseSeverity),
    required: true,
    index: true
  })
  severity: DiseaseSeverity;

  @Prop({ 
    type: [Object],
    required: true,
    validate: {
      validator: function(symptoms: Symptom[]) {
        return symptoms.length > 0 && symptoms.length <= 50;
      },
      message: 'Disease must have between 1 and 50 symptoms'
    }
  })
  symptoms: Symptom[];

  @Prop({ 
    type: [Object],
    required: true,
    validate: {
      validator: function(precautions: Precaution[]) {
        return precautions.length > 0 && precautions.length <= 20;
      },
      message: 'Disease must have between 1 and 20 precautions'
    }
  })
  precautions: Precaution[];

  @Prop({ 
    type: [Object],
    default: []
  })
  treatments: Treatment[];

  @Prop({ 
    type: [String],
    default: []
  })
  riskFactors: string[];

  @Prop({ 
    type: [String],
    default: []
  })
  complications: string[];

  @Prop({ 
    type: [String],
    default: []
  })
  diagnosticTests: string[];

  @Prop({ 
    type: [String],
    default: []
  })
  specialists: string[];

  @Prop({ 
    type: [String],
    default: []
  })
  tags: string[];

  @Prop({ 
    type: Object,
    default: {}
  })
  statistics: {
    prevalence?: number; // Percentage of population affected
    mortalityRate?: number; // Death rate if applicable
    recoveryRate?: number; // Recovery rate
    averageAge?: number; // Average age of onset
  };

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

export const DiseaseSchema = SchemaFactory.createForClass(Disease);

// Add indexes for better query performance
DiseaseSchema.index({ name: 1 });
DiseaseSchema.index({ category: 1, severity: 1 });
DiseaseSchema.index({ 'symptoms.name': 1 });
DiseaseSchema.index({ tags: 1 });
DiseaseSchema.index({ createdAt: -1 });
DiseaseSchema.index({ 'statistics.prevalence': -1 });
