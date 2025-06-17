import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document, Schema as MongooseSchema, Types } from 'mongoose';
import { User } from '../../auth/entities/user.entity';

export enum MessageSender {
  USER = 'user',
  BOT = 'bot',
}

export type ChatMessageDocument = ChatMessage & Document;

@Schema({ timestamps: { createdAt: 'timestamp' } })
export class ChatMessage {
  @Prop({
    type: String,
    enum: Object.values(MessageSender),
    required: true
  })
  sender: MessageSender;

  @Prop({ required: true })
  content: string;

  @Prop({ type: [Object], default: [] })
  diseases: any[];

  @Prop({ type: MongooseSchema.Types.ObjectId, ref: 'User', required: true })
  userId: Types.ObjectId;

  @Prop()
  timestamp: Date;
}

export const ChatMessageSchema = SchemaFactory.createForClass(ChatMessage);
