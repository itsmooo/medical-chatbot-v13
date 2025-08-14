import { Document } from 'mongoose';
export declare enum DiseaseCategory {
    INFECTIOUS = "infectious",
    CARDIOVASCULAR = "cardiovascular",
    RESPIRATORY = "respiratory",
    NEUROLOGICAL = "neurological",
    ENDOCRINE = "endocrine",
    GASTROINTESTINAL = "gastrointestinal",
    MUSCULOSKELETAL = "musculoskeletal",
    DERMATOLOGICAL = "dermatological",
    PSYCHIATRIC = "psychiatric",
    ONCOLOGICAL = "oncological",
    OTHER = "other"
}
export declare enum DiseaseSeverity {
    MILD = "mild",
    MODERATE = "moderate",
    SEVERE = "severe",
    CRITICAL = "critical"
}
export interface Symptom {
    name: string;
    description: string;
    frequency: number;
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
    effectiveness: number;
    sideEffects?: string[];
}
export type DiseaseDocument = Disease & Document;
export declare class Disease {
    name: string;
    description: string;
    category: DiseaseCategory;
    severity: DiseaseSeverity;
    symptoms: Symptom[];
    precautions: Precaution[];
    treatments: Treatment[];
    riskFactors: string[];
    complications: string[];
    diagnosticTests: string[];
    specialists: string[];
    tags: string[];
    statistics: {
        prevalence?: number;
        mortalityRate?: number;
        recoveryRate?: number;
        averageAge?: number;
    };
    metadata?: Record<string, any>;
    createdAt: Date;
    updatedAt: Date;
}
export declare const DiseaseSchema: import("mongoose").Schema<Disease, import("mongoose").Model<Disease, any, any, any, Document<unknown, any, Disease, any, {}> & Disease & {
    _id: import("mongoose").Types.ObjectId;
} & {
    __v: number;
}, any>, {}, {}, {}, {}, import("mongoose").DefaultSchemaOptions, Disease, Document<unknown, {}, import("mongoose").FlatRecord<Disease>, {}, import("mongoose").ResolveSchemaOptions<import("mongoose").DefaultSchemaOptions>> & import("mongoose").FlatRecord<Disease> & {
    _id: import("mongoose").Types.ObjectId;
} & {
    __v: number;
}>;
