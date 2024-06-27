import { 
  Controller,
  Get,
  NotFoundException,
  Query,
  InternalServerErrorException,
  BadRequestException } from '@nestjs/common';
import { IncomeDistService } from './income-dist.service';

// '/income-dist' 경로로 들어오는 요청 처리 
@Controller('income-dist')
export class IncomeDistController {
  // 비즈니스 로직인 서비스 계층 호출 
  constructor(private readonly incomeDistService: IncomeDistService) {}
  
  @Get()
  // find 메서드 : 해당 시군구, 읍면동의 소득 순위를 반환 
  async find(
    @Query('sido') sido_name: string,
    @Query('sigungu') sigungu_name: string, 
    @Query('emd') emd_name?: string
  ) {

    try {
      // 시도만 입력받았을 때
      if ( !sigungu_name || (!sigungu_name && !emd_name) ) 
        throw new BadRequestException('sigungu or sigungu + emd parameters are required')

      // 시도, 시군구, 읍면동 모두 제공된 경우
      if (emd_name) {
        const result = await this.incomeDistService.find(sido_name, sigungu_name, emd_name);
        return result;
      }
      // 시도와 시군구만 제공된 경우 
      else {
        const result = await this.incomeDistService.find(sido_name, sigungu_name);
        return result;
    } 
  }catch (error) {
      if (error instanceof NotFoundException || error instanceof BadRequestException) {
        throw error;
      } else {
        throw new InternalServerErrorException(`An unexpected error occurred! ${error.message}`);
    }
  }
}
}

// '/income-dist-xy' 경로로 들어오는 요청 처리 
@Controller('income-dist-xy')
export class IncomeDistXyController {
  // 비즈니스 로직인 서비스 계층 호출 
  constructor(private readonly incomeDistService: IncomeDistService) {}
  @Get()
  // findGeo 메서드 : 해당 시군구, 읍면동의 좌표 반환 
  async findGeo(
    @Query('sido') sido_name: string,
    @Query('sigungu') sigungu_name: string,
    @Query('emd') emd_name?: string
  ){
    try {
      // 시도만 입력받았을 때
      if ( !sigungu_name || (!sigungu_name && !emd_name) ) 
        throw new BadRequestException('sigungu or sigungu + emd parameters are required')
      if (emd_name){
        const result = await this.incomeDistService.findGeo(sido_name, sigungu_name, emd_name)
        return result;
      }
      else {
        const result = await this.incomeDistService.findGeo(sido_name, sigungu_name);
        return result;
      }
    } 
    catch (error) {
      if (error instanceof NotFoundException || error instanceof BadRequestException) {
        throw error;
      } else {
        throw new InternalServerErrorException(`An unexpected error occured! ${error.message}`);
      }
    }
  }
  }