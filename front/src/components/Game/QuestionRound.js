import React from 'react';
import { useParams } from 'react-router-dom';

const QuestionRound = () => {
    const { matchId, roundNumber } = useParams();
    return <div>Question Round {roundNumber} for Match {matchId}</div>;
};

export default QuestionRound;
