import { IsNotEmpty, IsOptional, IsString } from "class-validator";

export class FindIncomeDistDto {
    @IsNotEmpty()
    @IsString()
    sido: string;

    @IsNotEmpty()
    @IsString()
    sigungu: string;

    @IsOptional()
    @IsString()
    emd?: string;
}
