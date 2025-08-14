import { ChatService } from './chat.service';
import { ChatMessageDto } from './dto/chat-message.dto';
export declare class ChatController {
    private readonly chatService;
    constructor(chatService: ChatService);
    processMessage(chatMessageDto: ChatMessageDto, req: any): Promise<any>;
    getChatHistory(req: any): Promise<(import("mongoose").Document<unknown, {}, import("./entities/chat-message.entity").ChatMessageDocument, {}, {}> & import("./entities/chat-message.entity").ChatMessage & import("mongoose").Document<unknown, any, any, Record<string, any>, {}> & Required<{
        _id: unknown;
    }> & {
        __v: number;
    })[]>;
    getAllChatHistory(userId: string): Promise<(import("mongoose").Document<unknown, {}, import("./entities/chat-message.entity").ChatMessageDocument, {}, {}> & import("./entities/chat-message.entity").ChatMessage & import("mongoose").Document<unknown, any, any, Record<string, any>, {}> & Required<{
        _id: unknown;
    }> & {
        __v: number;
    })[]>;
}
