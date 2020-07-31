import configargparse
import signal
import glob
import pprint
from subprocess import Popen, STDOUT, PIPE


def get_list_of_maps() -> str:
    maps = [path[path.index('practice'):] for path in glob.glob(
        '../server/game_presets/practice*')]
    return maps


def display_list_of_maps():
    pp = pprint.PrettyPrinter(indent=4)

    print('Here\'s a list of maps that you can use. Some of them are for 2 players, and others for 4 players.\n')
    pp.pprint(get_list_of_maps())


splash = ''' 
██████╗ ██╗     ██╗████████╗███████╗    ██████╗  ██████╗ ██████╗  ██████╗ 
██╔══██╗██║     ██║╚══██╔══╝╚══███╔╝    ╚════██╗██╔═████╗╚════██╗██╔═████╗
██████╔╝██║     ██║   ██║     ███╔╝      █████╔╝██║██╔██║ █████╔╝██║██╔██║
██╔══██╗██║     ██║   ██║    ███╔╝      ██╔═══╝ ████╔╝██║██╔═══╝ ████╔╝██║
██████╔╝███████╗██║   ██║   ███████╗    ███████╗╚██████╔╝███████╗╚██████╔╝
╚═════╝ ╚══════╝╚═╝   ╚═╝   ╚══════╝    ╚══════╝ ╚═════╝ ╚══════╝ ╚═════╝ 
                                                                          

Go to https://2020.blitz.codes to start your journey.
That's one small step for man, one giant leap for ... mankind?

Use "docker run -p 8765:8765 -p 8080:8080 -it blitzmmxx/play --help" to get a list of commands.
'''

print(splash)
parser = configargparse.ArgumentParser(
    description="Coveo Blitz2020 local setup.")

parser.add_argument('--min_nb_players',
                    help="Set a minimum number of players. The game will wait to reach that number before starting.",
                    type=int, default=1)

parser.add_argument('--max_nb_ticks',
                    help="Set a maximum number of game ticks.",
                    type=int, default=100)

parser.add_argument('--no_ui',
                    help="Specify if a UI should be served along with the game server.",
                    action='store_false')

parser.add_argument('--list_maps',
                    help="Get the list of available maps to pratice", action='store_true')

parser.add_argument('--map',
                    help="Selects the map you wish to play on",
                    type=str,
                    default=None)

args = parser.parse_args()

if args.list_maps:
    display_list_of_maps()
    exit()


if args.map:
    maps = get_list_of_maps()

    try:
        maps.index(args.map)
    except ValueError:
        print(f' !! The map "{args.map}" doesn\'t exists !! \n')
        display_list_of_maps()
        exit()


if args.no_ui:
    print('Web UI started on port 8080 !')
    print('Got to http://localhost:8080/viewer.html to see what your bot is doing')
    print('or use http://localhost:8080/human_bot.html to play against it (and hope he\'ll beat you)!\n')

    uiProcess = Popen(['python', '-m', 'http.server', '8080'], cwd='ui/dist',
                      stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=False)

options = [
    './blitz2020',
    '--min_nb_players', str(args.min_nb_players),
    '--max_nb_ticks', str(args.max_nb_ticks),
    '--server_address', '0.0.0.0',
    '--game_delay', '250',
    '--move_timeout', '500']

if args.map:
    options.append('--game_config')
    options.append(args.map)

iteration = 0

while True:
    serverProcess = Popen([*options,
                           '--record_path',
                           f'/replays/replay-{iteration}.json'],
                          stdin=PIPE, shell=False)
    serverProcess.wait()

    iteration += 1
