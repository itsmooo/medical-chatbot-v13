import { Document, Schema as MongooseSchema, Types } from 'mongoose';
export declare enum MessageSender {
    USER = "user",
    BOT = "bot"
}
export declare enum MessageType {
    TEXT = "text",
    SYMPTOM_INPUT = "symptom_input",
    DISEASE_PREDICTION = "disease_prediction",
    FOLLOW_UP = "follow_up",
    ERROR = "error"
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
export declare class ChatMessage {
    sender: MessageSender;
    messageType: MessageType;
    content: string;
    diseases: DiseasePrediction[];
    symptomInput?: SymptomInput;
    userId: Types.ObjectId;
    replyTo?: Types.ObjectId;
    replies: Types.ObjectId[];
    isRead: boolean;
    isArchived: boolean;
    timestamp: Date;
    updatedAt: Date;
    metadata?: Record<string, any>;
}
export declare const ChatMessageSchema: MongooseSchema<ChatMessage, import("mongoose").Model<ChatMessage, any, any, any, Document<unknown, any, ChatMessage, any, {}> & ChatMessage & {
    _id: Types.ObjectId;
} & {
    __v: number;
}, any>, {}, {}, {}, {}, import("mongoose").DefaultSchemaOptions, ChatMessage, Document<unknown, {}, import("mongoose").FlatRecord<ChatMessage>, {}, import("mongoose").ResolveSchemaOptions<import("mongoose").DefaultSchemaOptions>> & import("mongoose").FlatRecord<ChatMessage> & {
    _id: Types.ObjectId;
} & {
    __v: number;
}>;
