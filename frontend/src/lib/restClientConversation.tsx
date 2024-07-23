import { BACKENDURL } from "@/consts/const";
import { Message } from "@/types/conversation"

interface CreateConversationPayload {
  id: string
}

interface GetConversationPayload {
  id: string
  messages: Message[]
}


interface GetConversationReturnType {
  messages: Message[];
}

class RestClient {
  private async get(endpoint: string) {
     const url = BACKENDURL + endpoint
    const res = await fetch(url)

    if (!res.ok) {
      throw new Error(`Http error! status: ${res.status}`);
    }
    return res;
  }

  private async post(endpoint: string, body?: any) {

    const url = BACKENDURL + endpoint;
    const res = await fetch(url, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(body)
    })

    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`)
    }
    return res;
  }

  public async createConversation(): Promise<string>  {
    const endpoint ="/api/conversation/";
    const res = await this.post(endpoint)
    const data = (await res.json()) as CreateConversationPayload
    return data.id
  }

  public async fetchConversation(conversationID: string): Promise<GetConversationReturnType> {
    const endpoint = `/api/conversation/${conversationID}`
    const res = await this.get(endpoint)
    const data = (await res.json()) as GetConversationPayload

    return {
      messages: data.messages
    }
  }
}


export const conversationClient = new RestClient()