export interface AnalysisResult {
  label: 'Hate Speech' | 'Non Hate Speech';
  probability: number;
  processed_text: string;
}
