import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Chess } from 'chess.js';


import { AiService } from './ai.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  game = new Chess();

  board: string[][] = [];

  selected: { i: number, j: number } | null = null;
  possibleMoves: string[] = [];

  recommendations: string[] = [];
  context: string = "";
  videos: any[] = [];

  evaluation: { score: number; best_move: string } | null = null;
  bestMove: string = "";

 
  constructor(private aiService: AiService) {}

  ngOnInit() {
    this.updateBoard();
    this.callAI();
  }

  updateBoard() {
    const board = this.game.board();

    this.board = board.map(row =>
      row.map(cell => cell ? cell.type : "")
    );
  }

  indexToSquare(i: number, j: number): string {
    const files = "abcdefgh";
    return files[j] + (8 - i);
  }

  selectSquare(i: number, j: number) {
    const square = this.indexToSquare(i, j);

    if (!this.selected) {
      this.selected = { i, j };

      this.possibleMoves = this.game.moves({
        square: square as any,
        verbose: true
      }).map(m => m.to);

      return;
    }

    const from = this.indexToSquare(this.selected.i, this.selected.j);
    const to = square;

    const move = this.game.move({ from, to });

    if (move) {
      this.updateBoard();
      this.callAI();
    }

    this.selected = null;
    this.possibleMoves = [];
  }

  playMove(move: string) {
    this.game.move(move);
    this.updateBoard();
    this.callAI();
  }

  callAI() {
    const fen = this.game.fen();

    
    this.aiService.getMoves(fen).subscribe({
      next: (res) => {
        this.recommendations = res.moves || [];
        this.context = res.context || "";
        this.videos = res.videos || [];
        this.evaluation = res.evaluation;
        this.bestMove = res.best_move;
      },
      error: (err) => console.error(err)
    });
  }
}