export interface AnswerData {
    id: string;
    answer: string;
}

export interface QuestionData {
    id: string;
    question: string;
    answers: AnswerData[];
}

export interface StoryData {
    story: string | null;
    vote: number | null;
}

export interface SiteInfoData {
    stories: StoryData[];
    answered: string[];
    questions: QuestionData[];
    story: StoryData;
}

export interface ItemData {
    id: number;
    name: string;
    address: string;
    latlng: [number, number];
    data: Record<string, string>;
    suburb: string;
}
