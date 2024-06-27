import { Test, TestingModule } from '@nestjs/testing';
import { IncomeDistController } from './income-dist.controller';
import { IncomeDistXyController } from './income-dist.controller';
import { IncomeDistService } from './income-dist.service';

describe('IncomeDistController', () => {
  let controller: IncomeDistController;
  let controller2: IncomeDistXyController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [IncomeDistController],
      providers: [IncomeDistService],
    }).compile();

    controller = module.get<IncomeDistController>(IncomeDistController);
    controller2 = module.get<IncomeDistXyController>(IncomeDistXyController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
    expect(controller2).toBeDefined();
  });
});
