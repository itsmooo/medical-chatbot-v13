"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __param = (this && this.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};
var ChatService_1;
Object.defineProperty(exports, "__esModule", { value: true });
exports.ChatService = void 0;
const common_1 = require("@nestjs/common");
const mongoose_1 = require("@nestjs/mongoose");
const mongoose_2 = require("mongoose");
const model_api_service_1 = require("../symptom-analyzer/model-api.service");
const chat_message_entity_1 = require("./entities/chat-message.entity");
let ChatService = ChatService_1 = class ChatService {
    modelApiService;
    chatMessageModel;
    logger = new common_1.Logger(ChatService_1.name);
    constructor(modelApiService, chatMessageModel) {
        this.modelApiService = modelApiService;
        this.chatMessageModel = chatMessageModel;
    }
    async processMessage(message, userId = 'anonymous') {
        try {
            await this.addMessageToHistory(userId, chat_message_entity_1.MessageSender.USER, message);
            const analysis = await this.modelApiService.predictDisease(message, userId);
            await this.addMessageToHistory(userId, chat_message_entity_1.MessageSender.BOT, analysis.response, analysis.diseases);
            return analysis;
        }
        catch (error) {
            this.logger.error(`Error processing message: ${error.message}`);
            const fallbackResponse = "I'm sorry, I couldn't analyze your symptoms properly. Could you provide more details about how you're feeling?";
            await this.addMessageToHistory(userId, chat_message_entity_1.MessageSender.BOT, fallbackResponse);
            return {
                response: fallbackResponse,
                diseases: [],
                error: error.message,
            };
        }
    }
    async getChatHistory(userId = 'anonymous') {
        return this.chatMessageModel.find({
            userId: userId !== 'anonymous' ? new mongoose_2.Types.ObjectId(userId) : userId
        })
            .sort({ timestamp: 1 })
            .exec();
    }
    async getAllChatHistory() {
        return this.chatMessageModel.find()
            .sort({ timestamp: 1 })
            .populate('userId', 'name email')
            .exec();
    }
    async addMessageToHistory(userId, sender, content, diseases = []) {
        const chatMessage = new this.chatMessageModel({
            sender,
            content,
            userId: userId !== 'anonymous' ? new mongoose_2.Types.ObjectId(userId) : userId,
            diseases: sender === chat_message_entity_1.MessageSender.BOT && diseases.length > 0 ? diseases : [],
        });
        return chatMessage.save();
    }
};
exports.ChatService = ChatService;
exports.ChatService = ChatService = ChatService_1 = __decorate([
    (0, common_1.Injectable)(),
    __param(1, (0, mongoose_1.InjectModel)(chat_message_entity_1.ChatMessage.name)),
    __metadata("design:paramtypes", [model_api_service_1.ModelApiService,
        mongoose_2.Model])
], ChatService);
//# sourceMappingURL=chat.service.js.map