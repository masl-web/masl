import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";

const useStyles = makeStyles({
  root: {
    Width: "100%",
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

const SampleOption = ({ no }) => {
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
          {no}번 옵션
        </Typography>
        <br />
        <Typography variant="body2" component="p">
          <br />
          <br />
        </Typography>
      </CardContent>
    </Card>
  );
};

export default SampleOption;
