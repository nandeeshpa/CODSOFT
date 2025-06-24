let board = ["", "", "", "", "", "", "", "", ""];
let human = "O";
let ai = "X";
let currentPlayer = human;

const boardEl = document.getElementById("board");
const statusEl = document.getElementById("status");

function drawBoard() {
  boardEl.innerHTML = "";
  board.forEach((cell, i) => {
    const cellEl = document.createElement("div");
    cellEl.classList.add("cell");
    cellEl.textContent = cell;
    cellEl.addEventListener("click", () => handleClick(i));
    boardEl.appendChild(cellEl);
  });
}

function handleClick(index) {
  if (board[index] !== "" || isGameOver()) return;
  board[index] = human;
  currentPlayer = ai;
  drawBoard();
  if (!isGameOver()) {
    let bestMove = minimax(board, 0, true).index;
    board[bestMove] = ai;
    currentPlayer = human;
    drawBoard();
  }
  checkWinner();
}

function isGameOver() {
  return checkWinner() || board.every(cell => cell !== "");
}

function checkWinner() {
  const winPatterns = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
  ];
  for (let pattern of winPatterns) {
    let [a, b, c] = pattern;
    if (board[a] && board[a] === board[b] && board[b] === board[c]) {
      statusEl.textContent = `${board[a]} wins!`;
      return true;
    }
  }
  if (board.every(cell => cell !== "")) {
    statusEl.textContent = "It's a draw!";
    return true;
  }
  statusEl.textContent = "";
  return false;
}

function minimax(newBoard, depth, isMaximizing) {
  if (checkWin(newBoard, ai)) return { score: 10 - depth };
  if (checkWin(newBoard, human)) return { score: depth - 10 };
  if (newBoard.every(cell => cell !== "")) return { score: 0 };

  let moves = [];

  newBoard.forEach((cell, i) => {
    if (cell === "") {
      let move = {};
      move.index = i;
      newBoard[i] = isMaximizing ? ai : human;

      let result = minimax(newBoard, depth + 1, !isMaximizing);
      move.score = result.score;
      newBoard[i] = "";
      moves.push(move);
    }
  });

  return isMaximizing
    ? moves.reduce((best, move) => move.score > best.score ? move : best)
    : moves.reduce((best, move) => move.score < best.score ? move : best);
}

function checkWin(board, player) {
  const winPatterns = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
  ];
  return winPatterns.some(pattern =>
    pattern.every(index => board[index] === player)
  );
}

function restartGame() {
  board = ["", "", "", "", "", "", "", "", ""];
  currentPlayer = human;
  drawBoard();
  statusEl.textContent = "";
}

drawBoard();
