import { Entity, Column, PrimaryGeneratedColumn, CreateDateColumn, ManyToOne, JoinColumn } from 'typeorm';
import { User } from '../../auth/entities/user.entity';

@Entity()
export class Prediction {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column('text')
  symptoms: string;

  @Column('json')
  diseases: any[];

  @Column('text')
  response: string;

  @ManyToOne(() => User, { eager: false })
  @JoinColumn({ name: 'userId' })
  user: User;

  @Column()
  userId: string;

  @CreateDateColumn()
  createdAt: Date;
}
