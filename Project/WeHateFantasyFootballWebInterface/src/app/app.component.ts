import { Component } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { concatMap, map, Observable } from 'rxjs';
import { PageEvent } from '@angular/material/paginator';

export interface SentimentData {
  image: string;
  name: string;
  projectedPoints: string;
  sentiment: string;
  numOfDataPoints: string;
  mostPositiveComment: string;
  mostPositiveCommentScore: string;
  mostNegativeComment: string;
  mostNegativeCommentScore: string;
  position: string;
  actualPoints: string;
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  pageIndex: number = 0;

  playerDataAndNames$: Observable<Map<string, string>>;
  currentlyDisplayedTable$: Observable<SentimentData[]> = this.http.get('assets/1.csv', {responseType: 'text'}).pipe(
    concatMap(data => {
      return this.convertSentimentCsvToObject(data);
    })
  );

  constructor(private http: HttpClient) {
    // Map for getting Player ID for the headshot
    this.playerDataAndNames$ = this.http.get('assets/playersNamesAndIds.csv', {responseType: 'text'}).pipe(
      map(data => {
          let csvToArray: string[] = data.split("\n");
          let playerMap = new Map<string, string>();
          csvToArray.forEach(row => {
            let nameAndId: string[] = row.split(",");
            playerMap.set(nameAndId[0], nameAndId[1]);
          });
          return playerMap;
      })
    );
  }

  private convertSentimentCsvToObject(data: string): Observable<SentimentData[]> {
    return this.playerDataAndNames$.pipe(
      map(playerMap => {
        let sentimentData: SentimentData[] = []
        let re = /,(?=[^"]*"[^"]*(?:"[^"]*"[^"]*)*$)/gm;
        data = data.replace(re, "");
        let csvToArray: string[] = data.split("\n");
        let skipFirstRow: boolean = true;
        csvToArray.forEach(row => {
          if(!skipFirstRow) {
            let rowData: string[] = row.split(",");
            let data: SentimentData = {
              image: `https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/${playerMap.get(rowData[0])}.png&w=96&h=70&cb=1`,
              name: rowData[0],
              projectedPoints: rowData[3],
              sentiment: rowData[4],
              numOfDataPoints: rowData[5],
              mostPositiveComment: rowData[7],
              mostPositiveCommentScore: rowData[8],
              mostNegativeComment: rowData[9],
              mostNegativeCommentScore: rowData[10],
              position: rowData[11],
              actualPoints: rowData[12]
            }
            if (data.image) {
              sentimentData.push(data);
            }
          } else {
            skipFirstRow = false;
          }
        });

        return sentimentData
      })
    );
  }

  handlePageEvent(e: PageEvent) {
    this.pageIndex = e.pageIndex;
    this.currentlyDisplayedTable$ = this.http.get(`assets/${this.pageIndex+1}.csv`, {responseType: 'text'}).pipe(
      concatMap(data => {
        return this.convertSentimentCsvToObject(data);
      })
    );
  }

  title = 'WeHateFantasyFootballWebInterface';
  displayedColumns: string[] = ['image', 'name', 'position', 'numOfDataPoints', 'actualPoints', 'projectedPoints', 'sentiment', 'mostPositiveComment', 'mostNegativeComment'];
}
