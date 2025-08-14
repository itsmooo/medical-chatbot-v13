import { Model } from 'mongoose';
import { ModelApiService } from '../symptom-analyzer/model-api.service';
import { ChatMessage, ChatMessageDocument } from './entities/chat-message.entity';
export declare class ChatService {
    private readonly modelApiService;
    private chatMessageModel;
    private readonly logger;
    constructor(modelApiService: ModelApiService, chatMessageModel: Model<ChatMessageDocument>);
    processMessage(message: string, userId?: string): Promise<any>;
    getChatHistory(userId?: string): Promise<(import("mongoose").Document<unknown, {}, ChatMessageDocument, {}, {}> & ChatMessage & import("mongoose").Document<unknown, any, any, Record<string, any>, {}> & Required<{
        _id: unknown;
    }> & {
        __v: number;
    })[]>;
    getAllChatHistory(): Promise<(import("mongoose").Document<unknown, {}, ChatMessageDocument, {}, {}> & ChatMessage & import("mongoose").Document<unknown, any, any, Record<string, any>, {}> & Required<{
        _id: unknown;
    }> & {
        __v: number;
    })[]>;
    private addMessageToHistory;
}
