from react.graph import app

if __name__ == "__main__":
    print("Hello ReAct with LangGraph")
    config = {"configurable": {"thread_id": "89"}}

    for event in app.stream(
        {"input": "current weather in New York? In Celsius-. Then triple it"},
        config,
    ):
        for node, values in event.items():
            print(f"Receiving update from node: '{node}'")
            print(values)
            print("\n\n")
