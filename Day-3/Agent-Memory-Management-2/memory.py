class Memory:
    async def auto_save_to_memory(callback_context):
        await callback_context._invocation_context.memory_service.add_session_to_memory(
                callback_context._invocation_context.session
        )
