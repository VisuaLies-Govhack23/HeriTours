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
