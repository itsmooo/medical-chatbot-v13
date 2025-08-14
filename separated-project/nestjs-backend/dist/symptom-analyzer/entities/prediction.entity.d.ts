import { Document, Schema as MongooseSchema, Types } from 'mongoose';
export declare enum PredictionStatus {
    PENDING = "pending",
    PROCESSING = "processing",
    COMPLETED = "completed",
    FAILED = "failed"
}
export declare enum PredictionAccuracy {
    LOW = "low",
    MEDIUM = "medium",
    HIGH = "high"
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
export declare class Prediction {
    symptoms: string;
    diseases: DiseaseResult[];
    response: string;
    userId: Types.ObjectId;
    status: PredictionStatus;
    accuracy: PredictionAccuracy;
    symptomAnalysis?: SymptomAnalysis;
    modelPerformance?: ModelPerformance;
    tags: string[];
    isFollowUpRequired: boolean;
    followUpDate?: Date;
    followUpNotes?: string;
    metadata?: Record<string, any>;
    createdAt: Date;
    updatedAt: Date;
}
export declare const PredictionSchema: MongooseSchema<Prediction, import("mongoose").Model<Prediction, any, any, any, Document<unknown, any, Prediction, any, {}> & Prediction & {
    _id: Types.ObjectId;
} & {
    __v: number;
}, any>, {}, {}, {}, {}, import("mongoose").DefaultSchemaOptions, Prediction, Document<unknown, {}, import("mongoose").FlatRecord<Prediction>, {}, import("mongoose").ResolveSchemaOptions<import("mongoose").DefaultSchemaOptions>> & import("mongoose").FlatRecord<Prediction> & {
    _id: Types.ObjectId;
} & {
    __v: number;
}>;
