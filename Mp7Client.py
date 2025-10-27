from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
    CommonContext, server_loop
import asyncio
import Utils

class MarioParty7Context(CommonContext):
    game = "Mario Party 7"

def main(connect= None, password= None):
    Utils.init_logging("MarioParty7Client", exception_logger="Client")

    async def _main(connect, password):
        ctx = MarioParty7Context(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        # game start...

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()


    import colorama

    colorama.init()
    asyncio.run(_main(connect, password))
    colorama.deinit()

if __name__ == "__main__":
    parser = get_base_parser(description="Mario Party 7 Client, for text interfacing.")
    args, rest = parser.parse_known_args()
    main(args.connect, args.password)