sequenceDiagram
  participant Twilio
  participant AI_System as AI System
  participant Ngrok
  participant OpenAI_API as OpenAI API
  participant Special_Model as Special OpenAI Model
  Twilio->>AI_System: Initiate Call
  loop For Each Call
    
    Twilio-)Ngrok: Push Data via Ngrok
    Ngrok->>OpenAI_API: Connect for Question/Answer
    alt Need Special Model?
      OpenAI_API->>Special_Model: Invoke Special Model
      Special_Model-->>OpenAI_API: Critical Response
    end
    OpenAI_API-->>Twilio: Provide Answer
    OpenAI_API--X Twilio: Decide if Call Ends
  end
