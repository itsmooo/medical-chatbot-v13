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
Object.defineProperty(exports, "__esModule", { value: true });
exports.ChatMessageSchema = exports.ChatMessage = exports.MessageType = exports.MessageSender = void 0;
const mongoose_1 = require("@nestjs/mongoose");
const mongoose_2 = require("mongoose");
var MessageSender;
(function (MessageSender) {
    MessageSender["USER"] = "user";
    MessageSender["BOT"] = "bot";
})(MessageSender || (exports.MessageSender = MessageSender = {}));
var MessageType;
(function (MessageType) {
    MessageType["TEXT"] = "text";
    MessageType["SYMPTOM_INPUT"] = "symptom_input";
    MessageType["DISEASE_PREDICTION"] = "disease_prediction";
    MessageType["FOLLOW_UP"] = "follow_up";
    MessageType["ERROR"] = "error";
})(MessageType || (exports.MessageType = MessageType = {}));
let ChatMessage = class ChatMessage {
    sender;
    messageType;
    content;
    diseases;
    symptomInput;
    userId;
    replyTo;
    replies;
    isRead;
    isArchived;
    timestamp;
    updatedAt;
    metadata;
};
exports.ChatMessage = ChatMessage;
__decorate([
    (0, mongoose_1.Prop)({
        type: String,
        enum: Object.values(MessageSender),
        required: true,
        index: true
    }),
    __metadata("design:type", String)
], ChatMessage.prototype, "sender", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: String,
        enum: Object.values(MessageType),
        default: MessageType.TEXT,
        index: true
    }),
    __metadata("design:type", String)
], ChatMessage.prototype, "messageType", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        required: true,
        trim: true,
        maxlength: 2000
    }),
    __metadata("design:type", String)
], ChatMessage.prototype, "content", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: [Object],
        default: [],
        validate: {
            validator: function (diseases) {
                return diseases.length <= 10;
            },
            message: 'Cannot have more than 10 diseases per message'
        }
    }),
    __metadata("design:type", Array)
], ChatMessage.prototype, "diseases", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: Object,
        default: null
    }),
    __metadata("design:type", Object)
], ChatMessage.prototype, "symptomInput", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: mongoose_2.Schema.Types.ObjectId,
        ref: 'User',
        required: true,
        index: true
    }),
    __metadata("design:type", mongoose_2.Types.ObjectId)
], ChatMessage.prototype, "userId", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: mongoose_2.Schema.Types.ObjectId,
        ref: 'ChatMessage',
        default: null
    }),
    __metadata("design:type", mongoose_2.Types.ObjectId)
], ChatMessage.prototype, "replyTo", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: [mongoose_2.Schema.Types.ObjectId],
        ref: 'ChatMessage',
        default: []
    }),
    __metadata("design:type", Array)
], ChatMessage.prototype, "replies", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        default: false
    }),
    __metadata("design:type", Boolean)
], ChatMessage.prototype, "isRead", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        default: false
    }),
    __metadata("design:type", Boolean)
], ChatMessage.prototype, "isArchived", void 0);
__decorate([
    (0, mongoose_1.Prop)(),
    __metadata("design:type", Date)
], ChatMessage.prototype, "timestamp", void 0);
__decorate([
    (0, mongoose_1.Prop)(),
    __metadata("design:type", Date)
], ChatMessage.prototype, "updatedAt", void 0);
__decorate([
    (0, mongoose_1.Prop)({
        type: Object,
        default: {}
    }),
    __metadata("design:type", Object)
], ChatMessage.prototype, "metadata", void 0);
exports.ChatMessage = ChatMessage = __decorate([
    (0, mongoose_1.Schema)({
        timestamps: { createdAt: 'timestamp', updatedAt: 'updatedAt' },
        collection: 'chat_messages'
    })
], ChatMessage);
exports.ChatMessageSchema = mongoose_1.SchemaFactory.createForClass(ChatMessage);
exports.ChatMessageSchema.index({ userId: 1, timestamp: -1 });
exports.ChatMessageSchema.index({ sender: 1, timestamp: -1 });
exports.ChatMessageSchema.index({ messageType: 1, timestamp: -1 });
exports.ChatMessageSchema.index({ isRead: 1, userId: 1 });
exports.ChatMessageSchema.index({ isArchived: 1, userId: 1 });
//# sourceMappingURL=chat-message.entity.js.map