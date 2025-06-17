import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document, Schema as MongooseSchema, Types } from 'mongoose';
import { User } from '../../auth/entities/user.entity';

export type PredictionDocument = Prediction & Document;

@Schema({ timestamps: true })
export class Prediction {
  @Prop({ required: true })
  symptoms: string;

  @Prop({ type: [Object], default: [] })
  diseases: any[];

  @Prop({ required: true })
  response: string;

  @Prop({ type: MongooseSchema.Types.ObjectId, ref: 'User', required: true })
  userId: Types.ObjectId;

  @Prop()
  createdAt: Date;
}

export const PredictionSchema = SchemaFactory.createForClass(Prediction);
