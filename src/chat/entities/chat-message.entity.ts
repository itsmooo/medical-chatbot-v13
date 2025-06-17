import { Entity, Column, PrimaryGeneratedColumn, CreateDateColumn, ManyToOne, JoinColumn } from 'typeorm';
import { User } from '../../auth/entities/user.entity';

export enum MessageSender {
  USER = 'user',
  BOT = 'bot',
}

@Entity()
export class ChatMessage {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({
    type: 'enum',
    enum: MessageSender,
  })
  sender: MessageSender;

  @Column('text')
  content: string;

  @Column('json', { nullable: true })
  diseases: any[];

  @ManyToOne(() => User, { eager: false })
  @JoinColumn({ name: 'userId' })
  user: User;

  @Column()
  userId: string;

  @CreateDateColumn()
  timestamp: Date;
}
