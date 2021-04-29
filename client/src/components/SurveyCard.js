import React from "react";
import { useHistory } from "react-router-dom";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";

const useStyles = makeStyles({
  root: {
    Width: "100%",
    minHeight: 260,
    marginTop: 20,
    marginLeft: 10,
    marginRight: 10,
    paddingTop: 40,
    borderRadius: 10,
    textAlign: "center",
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

  Button: {
    border: "none",
  },
});

// "#9370DB"
const SurveyCard = () => {
  const classes = useStyles();
  let history = useHistory();

  const onMove = () => {
    // window.location.replace("/userinfo");
    history.push({
      pathname: "/userinfo",
    });
  };

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
          마슬 찾아보기
        </Typography>
        <br />
        <Typography variant="body2" component="p">
          <Button
            variant="outlined"
            color="primary"
            onClick={onMove}
            style={{
              margin: 0,
              padding: 12,
              width: "80%",
              borderRadius: 10,
              fontSize: 16,
            }}
          >
            Start
          </Button>
          <br />
        </Typography>
      </CardContent>
    </Card>
  );
};

export default SurveyCard;
