import chess
import streamlit as st

from main import select_move


st.set_page_config(page_title="Alpha-Beta Chess", page_icon="♟", layout="wide")

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
}


def start_game(color):
    st.session_state.board = chess.Board()
    st.session_state.player_color = color
    st.session_state.move_history = []
    st.session_state.selected_square = None


def play_move(move):
    san = st.session_state.board.san(move)
    st.session_state.board.push(move)
    st.session_state.move_history.append(san)
    st.session_state.selected_square = None


def handle_square_click(square):
    board = st.session_state.board
    selected = st.session_state.selected_square
    if selected is None:
        piece = board.piece_at(square)
        if piece and piece.color == st.session_state.player_color and board.turn == piece.color:
            st.session_state.selected_square = square
        return

    if square == selected:
        st.session_state.selected_square = None
        return

    moves = [
        move for move in board.legal_moves
        if move.from_square == selected and move.to_square == square
    ]
    if moves:
        move = next((move for move in moves if move.promotion == chess.QUEEN), moves[0])
        play_move(move)
        return

    piece = board.piece_at(square)
    if piece and piece.color == st.session_state.player_color and board.turn == piece.color:
        st.session_state.selected_square = square
    else:
        st.session_state.selected_square = None


def material_score(board):
    score = 0
    for piece_type, value in PIECE_VALUES.items():
        score += len(board.pieces(piece_type, chess.WHITE)) * value
        score -= len(board.pieces(piece_type, chess.BLACK)) * value
    return score


def render_board(board):
    player_color = st.session_state.player_color
    ranks = range(7, -1, -1) if player_color == chess.WHITE else range(8)
    files = range(8) if player_color == chess.WHITE else range(7, -1, -1)
    selected = st.session_state.selected_square

    st.markdown(
        """
        <style>
        .block-container { max-width: 1280px; padding: 2rem 1.5rem 1rem; }
        .st-key-chess-board [data-testid="stVerticalBlock"] { gap: 0 !important; }
        [class*="st-key-square_"] button {
            width: 100%; height: auto; min-height: 0; aspect-ratio: 1;
            padding: 0; border: 0; border-radius: 2px;
            font-size: clamp(25px, 4vw, 48px); line-height: 1;
        }
        [class*="st-key-square_"] button p {
            font-size: clamp(25px, 4vw, 48px); line-height: 1;
        }
        @media (max-width: 700px) {
            .block-container { padding: 1.25rem 0.6rem 0.75rem; }
            [class*="st-key-square_"] button,
            [class*="st-key-square_"] button p { font-size: clamp(20px, 7vw, 36px); }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    board_container = st.container(key="chess-board")
    board_columns = board_container.columns([1] * 8, gap=None)
    for rank in ranks:
        for file_index, file in enumerate(files):
            square = chess.square(file, rank)
            square_name = chess.square_name(square)
            piece = board.piece_at(square)
            label = piece.unicode_symbol() if piece else " "
            key = f"square_{square_name}"
            light = (file + rank) % 2 == 1
            background = "#e7e5d8" if light else "#63816f"
            if square == selected:
                background = "#d5ad4a"
            piece_color = "#fbf8ed" if piece and piece.color == chess.WHITE else "#202923"
            piece_outline = "#31483d" if piece and piece.color == chess.WHITE else "#f1e7c9"
            st.markdown(
                f"<style>.st-key-{key} button{{background:{background};color:{piece_color};-webkit-text-stroke:0.65px {piece_outline};}}</style>",
                unsafe_allow_html=True,
            )
            with board_columns[file_index]:
                st.button(label, key=key, help=square_name, on_click=handle_square_click, args=(square,), use_container_width=True)

    for index, file in enumerate(files):
        with board_columns[index]:
            st.markdown(f"<div style='text-align:center;color:#626b67;padding-top:.35rem'>{chess.FILE_NAMES[file]}</div>", unsafe_allow_html=True)


if "board" not in st.session_state:
    st.session_state.side_choice = "White"
    start_game(chess.WHITE)

with st.sidebar:
    st.markdown("### Game settings")
    side_choice = st.selectbox("Play as", ["White", "Black"], key="side_choice")
    depth = st.slider("AI search depth", min_value=1, max_value=4, value=3)
    if st.button("New game", use_container_width=True):
        start_game(chess.WHITE if side_choice == "White" else chess.BLACK)
        st.rerun()
    st.caption("Moves promote to a queen automatically.")

chosen_color = chess.WHITE if side_choice == "White" else chess.BLACK
if chosen_color != st.session_state.player_color:
    start_game(chosen_color)

board = st.session_state.board
if board.turn != st.session_state.player_color and not board.is_game_over():
    with st.spinner("The engine is thinking..."):
        ai_move = select_move(board, depth=depth)
    if ai_move is not None:
        play_move(ai_move)
    board = st.session_state.board

st.markdown("# Alpha-Beta Chess")
st.caption("A chess match against a minimax engine with alpha-beta pruning.")

game_over = board.is_game_over()
left, right = st.columns([2.7, 1], gap="large")
with left:
    render_board(board)
with right:
    st.markdown("### Match")
    if game_over:
        st.success(f"Game over · {board.result()} · {board.outcome().termination.name.replace('_', ' ').title()}")
    elif board.is_check():
        st.warning("Check")
    st.metric("To move", "White" if board.turn else "Black")
    score = material_score(board)
    st.metric("Material balance", f"{score:+d} (White)")
    st.markdown("### Moves")
    if st.session_state.move_history:
        formatted_moves = []
        for index in range(0, len(st.session_state.move_history), 2):
            white_move = st.session_state.move_history[index]
            black_move = st.session_state.move_history[index + 1] if index + 1 < len(st.session_state.move_history) else "..."
            formatted_moves.append(f"{index // 2 + 1}. {white_move} {black_move}")
        st.code("\n".join(formatted_moves), language=None)
    else:
        st.caption("No moves yet.")