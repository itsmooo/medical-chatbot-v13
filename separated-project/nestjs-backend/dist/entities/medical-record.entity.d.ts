import { Document, Schema as MongooseSchema, Types } from 'mongoose';
export declare enum RecordType {
    SYMPTOM_RECORD = "symptom_record",
    DIAGNOSIS = "diagnosis",
    TREATMENT = "treatment",
    MEDICATION = "medication",
    LAB_RESULT = "lab_result",
    IMAGING = "imaging",
    SURGERY = "surgery",
    FOLLOW_UP = "follow_up",
    EMERGENCY = "emergency"
}
export declare enum RecordStatus {
    ACTIVE = "active",
    RESOLVED = "resolved",
    ONGOING = "ongoing",
    ARCHIVED = "archived"
}
export declare enum BloodType {
    A_POSITIVE = "A+",
    A_NEGATIVE = "A-",
    B_POSITIVE = "B+",
    B_NEGATIVE = "B-",
    AB_POSITIVE = "AB+",
    AB_NEGATIVE = "AB-",
    O_POSITIVE = "O+",
    O_NEGATIVE = "O-"
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
export declare class MedicalRecord {
    userId: Types.ObjectId;
    recordType: RecordType;
    status: RecordStatus;
    title: string;
    description: string;
    date: Date;
    vitalSigns?: VitalSigns;
    medications: Medication[];
    labResults: LabResult[];
    surgeries: Surgery[];
    allergies: string[];
    chronicConditions: string[];
    familyHistory: string[];
    lifestyleFactors: string[];
    tags: string[];
    attachments: string[];
    doctorNotes?: string;
    patientNotes?: string;
    metadata?: Record<string, any>;
    createdAt: Date;
    updatedAt: Date;
}
export declare const MedicalRecordSchema: MongooseSchema<MedicalRecord, import("mongoose").Model<MedicalRecord, any, any, any, Document<unknown, any, MedicalRecord, any, {}> & MedicalRecord & {
    _id: Types.ObjectId;
} & {
    __v: number;
}, any>, {}, {}, {}, {}, import("mongoose").DefaultSchemaOptions, MedicalRecord, Document<unknown, {}, import("mongoose").FlatRecord<MedicalRecord>, {}, import("mongoose").ResolveSchemaOptions<import("mongoose").DefaultSchemaOptions>> & import("mongoose").FlatRecord<MedicalRecord> & {
    _id: Types.ObjectId;
} & {
    __v: number;
}>;
