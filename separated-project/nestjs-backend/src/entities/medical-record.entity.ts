import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document, Schema as MongooseSchema, Types } from 'mongoose';
import { User } from '../auth/entities/user.entity';

export enum RecordType {
  SYMPTOM_RECORD = 'symptom_record',
  DIAGNOSIS = 'diagnosis',
  TREATMENT = 'treatment',
  MEDICATION = 'medication',
  LAB_RESULT = 'lab_result',
  IMAGING = 'imaging',
  SURGERY = 'surgery',
  FOLLOW_UP = 'follow_up',
  EMERGENCY = 'emergency'
}

export enum RecordStatus {
  ACTIVE = 'active',
  RESOLVED = 'resolved',
  ONGOING = 'ongoing',
  ARCHIVED = 'archived'
}

export enum BloodType {
  A_POSITIVE = 'A+',
  A_NEGATIVE = 'A-',
  B_POSITIVE = 'B+',
  B_NEGATIVE = 'B-',
  AB_POSITIVE = 'AB+',
  AB_NEGATIVE = 'AB-',
  O_POSITIVE = 'O+',
  O_NEGATIVE = 'O-'
}

export interface VitalSigns {
  bloodPressure?: {
    systolic: number;
    diastolic: number;
    unit: 'mmHg';
  };
  heartRate?: {
    value: number;
    unit: 'bpm';
  };
  temperature?: {
    value: number;
    unit: '°C' | '°F';
  };
  respiratoryRate?: {
    value: number;
    unit: 'breaths/min';
  };
  oxygenSaturation?: {
    value: number;
    unit: '%';
  };
  weight?: {
    value: number;
    unit: 'kg' | 'lbs';
  };
  height?: {
    value: number;
    unit: 'cm' | 'inches';
  };
}

export interface Medication {
  name: string;
  dosage: string;
  frequency: string;
  duration: string;
  startDate: Date;
  endDate?: Date;
  prescribedBy?: string;
  instructions: string;
  sideEffects?: string[];
  isActive: boolean;
}

export interface LabResult {
  testName: string;
  result: string;
  normalRange: string;
  unit: string;
  isAbnormal: boolean;
  date: Date;
  lab: string;
  orderedBy: string;
}

export interface Surgery {
  procedure: string;
  date: Date;
  surgeon: string;
  hospital: string;
  complications?: string[];
  recoveryTime?: string;
  notes?: string;
}

export type MedicalRecordDocument = MedicalRecord & Document;

@Schema({ 
  timestamps: true,
  collection: 'medical_records'
})
export class MedicalRecord {
  @Prop({ 
    type: MongooseSchema.Types.ObjectId, 
    ref: 'User', 
    required: true,
    index: true
  })
  userId: Types.ObjectId;

  @Prop({
    type: String,
    enum: Object.values(RecordType),
    required: true,
    index: true
  })
  recordType: RecordType;

  @Prop({
    type: String,
    enum: Object.values(RecordStatus),
    default: RecordStatus.ACTIVE,
    index: true
  })
  status: RecordStatus;

  @Prop({ 
    required: true,
    trim: true,
    maxlength: 500
  })
  title: string;

  @Prop({ 
    required: true,
    trim: true,
    maxlength: 2000
  })
  description: string;

  @Prop({ 
    type: Date,
    required: true
  })
  date: Date;

  @Prop({ 
    type: Object,
    default: null
  })
  vitalSigns?: VitalSigns;

  @Prop({ 
    type: [Object],
    default: []
  })
  medications: Medication[];

  @Prop({ 
    type: [Object],
    default: []
  })
  labResults: LabResult[];

  @Prop({ 
    type: [Object],
    default: []
  })
  surgeries: Surgery[];

  @Prop({ 
    type: [String],
    default: []
  })
  allergies: string[];

  @Prop({ 
    type: [String],
    default: []
  })
  chronicConditions: string[];

  @Prop({ 
    type: [String],
    default: []
  })
  familyHistory: string[];

  @Prop({ 
    type: [String],
    default: []
  })
  lifestyleFactors: string[];

  @Prop({ 
    type: [String],
    default: []
  })
  tags: string[];

  @Prop({ 
    type: [String],
    default: []
  })
  attachments: string[]; // File paths or URLs

  @Prop({ 
    type: String,
    default: null
  })
  doctorNotes?: string;

  @Prop({ 
    type: String,
    default: null
  })
  patientNotes?: string;

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

export const MedicalRecordSchema = SchemaFactory.createForClass(MedicalRecord);

// Add indexes for better query performance
MedicalRecordSchema.index({ userId: 1, date: -1 });
MedicalRecordSchema.index({ userId: 1, recordType: 1 });
MedicalRecordSchema.index({ userId: 1, status: 1 });
MedicalRecordSchema.index({ recordType: 1, date: -1 });
MedicalRecordSchema.index({ 'medications.name': 1 });
MedicalRecordSchema.index({ 'labResults.testName': 1 });
MedicalRecordSchema.index({ tags: 1 });
MedicalRecordSchema.index({ createdAt: -1 });
