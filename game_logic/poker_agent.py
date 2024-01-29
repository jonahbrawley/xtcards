def predict_ai_move(game_state_at_ai):
    print("\nAI State input:")
    for (key, value) in game_state_at_ai.items():
        print(f"key: {key}, value: {value}")
    print("AI action: call (hard-coded)\n")
    return "call"
