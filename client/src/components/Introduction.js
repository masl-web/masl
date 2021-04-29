import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";

const useStyles = makeStyles({
  root: {
    minWidth: "100%",
    minHeight: 260,
    marginTop: 20,
    marginLeft: 10,
    marginRight: 10,
    borderRadius: 10,
  },
  bullet: {
    display: "inline-block",
    margin: "0 2px",
    transform: "scale(0.8)",
  },
  title: {
    fontSize: 14,
  },
  pos: {
    marginBottom: 12,
  },
});

const Introduction = () => {
  const classes = useStyles();

  return (
    <Card className={classes.root}>
      <CardContent>
        <Typography
          className={classes.title}
          color="textSecondary"
          gutterBottom
        >
          나의 슬세권 찾기 서비스
        </Typography>
        <Typography variant="h5" component="h2">
          MASL
        </Typography>
        <br />
        <Typography variant="body2" component="p">
          &nbsp;&nbsp;마슬은 내가 살기 좋은 동네의 다양한 정보를 알려주는
          웹서비스입니다.
          <br />
          <br />
          &nbsp;&nbsp;거주지 추천 서비스에서 진화한 지역 주천 알고리즘과 다양한
          지역 정보를 알려주는 웹 서비스입니다.
        </Typography>
      </CardContent>
    </Card>
  );
};

export default Introduction;
