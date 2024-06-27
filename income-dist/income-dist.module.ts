import { Module } from '@nestjs/common';
import { DatabaseModule } from 'src/database/database.module';
import { IncomeDistController } from './income-dist.controller';
import { IncomeDistService } from './income-dist.service';
import { incomeDistProviders } from './income-dist.providers';
import { IncomeDistXyController } from './income-dist.controller';

@Module({ 
  imports: [ DatabaseModule ],
  controllers: [ IncomeDistController, IncomeDistXyController ],
  providers: [
    IncomeDistService,  // 비즈니스 로직 처리 
    ... incomeDistProviders,    // db 리포지토리 제공자 포함 
  ],
  exports: [IncomeDistService],
})
export class IncomeDistModule {}
