
export enum MESSAGE_STATUS {
  PENDING = "PENDING",
  SUCCESS = "SUCCESS",
  ERROR = "ERROR",
}

export enum ROLE {
  USER = "user",
  ASSISTANT = "assistant",
}

export interface hasId {
  id: string;
}

export interface Conversation extends hasId {
  messages?: Message[];
}


export interface Message extends hasId {
  content: string;
  role: ROLE;
  status: MESSAGE_STATUS;
  conversationID: string;
  created_at: Date;
}


export interface ParsedData {
  content?: string;
  status?: string;
}