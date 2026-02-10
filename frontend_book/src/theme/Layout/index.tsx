import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import type {Props} from '@theme/Layout';
import RagChatbot from '@site/src/components/RagChatbot';

export default function Layout(props: Props): React.ReactElement {
  return (
    <>
      <OriginalLayout {...props} />
      <RagChatbot />
    </>
  );
}